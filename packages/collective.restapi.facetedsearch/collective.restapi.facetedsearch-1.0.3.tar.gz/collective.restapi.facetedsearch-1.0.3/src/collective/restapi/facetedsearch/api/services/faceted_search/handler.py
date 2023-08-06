# -*- coding: utf-8 -*-
from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.utils import safe_iterable, safe_decode
from Missing import Missing
from pkg_resources import get_distribution
from pkg_resources import parse_version
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.search.handler import SearchHandler
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter
from zope.component import getUtility
from ZTUtils.Lazy import LazyCat
from inspect import signature
from plone import api

zcatalog_version = get_distribution("Products.ZCatalog").version
if parse_version(zcatalog_version) >= parse_version("5.1"):
    SUPPORT_NOT_UUID_QUERIES = True
else:
    SUPPORT_NOT_UUID_QUERIES = False


class FacetedSearchHandler(SearchHandler):
    """Executes a catalog search based on a query dict, and returns
    JSON compatible results.
    """

    def search(self, query=None):
        if query is None:
            query = {}
        if "fullobjects" in query:
            fullobjects = True
            del query["fullobjects"]
        else:
            fullobjects = False

        metadata_fields = query.pop("metadata_fields", [])
        if not isinstance(metadata_fields, list):
            metadata_fields = [metadata_fields]

        facets = query.pop("facets", None)
        if facets and not isinstance(facets, list):
            facets = [facets]

        facets_only = query.pop('facets_only', False)
        possible_facets = query.pop('possible_facets', False)
        # Remove batching params from query to get facets from all brains. We
        # do not have to re-add them because further processing is based on
        # request params, which we didn't touch.
        if facets:
            query.pop('b_size', None)
            query.pop('b_start', None)
        serializable_facets = None

        self._constrain_query_by_path(query)
        query = self._parse_query(query)
        lazy_resultset = self.catalog.searchResults(query)
        if facets:
            serializable_facets = getFacets(lazy_resultset, query, facets)
        results = self.getSerializableResults(lazy_resultset, self.request,
                                         fullobjects, facets_only)


        results["facets"] = serializable_facets
        if possible_facets:
            results["possible_facets"] = getPossibleFacets()

        return results

    def getSerializableResults(self, lazy_results, request, fullobjects, facets_only):
        return getSerializableResults(lazy_results, request, fullobjects, facets_only)


class FacetedQuerystringSearchHandler():
    """Executes a querybuilder based catalog search and returns JSON compatible
    results.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def search(self):
        """ Inspired by QuerystringSearchPost.reply()
        plone.restapi-7.0.0-py3.7.egg/plone/restapi/services/querystringsearch/get.py
        """
        data = json_body(self.request)
        query = data.get("query", None)
        b_start = int(data.get("b_start", 0))
        b_size = int(data.get("b_size", 25))
        sort_on = data.get("sort_on", None)
        sort_order = data.get("sort_order", None)
        limit = data.get("limit", None)
        if limit:
            try:
                limit = int(limit)
            except:
                raise Exception("limit must be an integer")
        fullobjects = data.get("fullobjects", False)
        facets = data.get("facets", [])
        facets_only = data.get('facets_only', False)
        possible_facets = data.get('possible_facets', False)
        if not isinstance(facets, list):
            facets = [facets]

        # if no query supplied, we assume that all child data of current context is requested
        if not query:
            site_path = api.portal.get().getPhysicalPath();
            context_path = self.context.getPhysicalPath()
            relative_path = context_path[len(site_path):]
            path = "/" + "/".join(relative_path)
            query = [{
                "i":"path",
                "o":"plone.app.querystring.operation.string.absolutePath",
                "v": path}]
            #raise Exception("No query supplied")

        sort_order = "descending" if sort_order else "ascending"

        querybuilder = getMultiAdapter(
            (self.context, self.request), name="querybuilderresults"
        )

        querybuilder_parameters = dict(
            query=query,
            brains=True,
            b_start=b_start,
            b_size=b_size,
            sort_on=sort_on,
            sort_order=sort_order,
            limit=limit,
        )
        # Exclude "self" content item from the results when ZCatalog supports NOT UUID
        # queries and it is called on a content object.
        if not IPloneSiteRoot.providedBy(self.context) and SUPPORT_NOT_UUID_QUERIES:
            querybuilder_parameters.update(
                dict(custom_query={"UID": {"not": self.context.UID()}})
            )

        lazy_resultset = querybuilder(**querybuilder_parameters)
        if lazy_resultset == []:
            lazy_resultset = LazyCat([])
        serializable_facets = getFacets(lazy_resultset, query, facets)
        results = self.getSerializableResults(lazy_resultset, self.request,
                                         fullobjects, facets_only)
        results["facets"] = serializable_facets
        if possible_facets:
            results["possible_facets"] = getPossibleFacets()

        return results

    def getSerializableResults(self, lazy_results, request, fullobjects, facets_only):
        return getSerializableResults(lazy_results, request, fullobjects, facets_only)


def getSerializableResults(lazy_results, request, fullobjects, facets_only):
    #import pdb; pdb.set_trace()
    if facets_only is not False:
        # Prepare result serialization on empty LazyMap
        empty_lazy = LazyCat([])
        results = getMultiAdapter(
                (empty_lazy, request), ISerializeToJson
            )(fullobjects=False)
        # We need to fix the items_total property
        results['items_total'] = lazy_results.actual_result_count
    else:
        results = getMultiAdapter(
                (lazy_results, request), ISerializeToJson
            )(fullobjects=fullobjects)
    return results


def getFacets(catalog_results, query, metadata=['portal_type']):
    fod = getFacetsOptionsDict(metadata, query)
    facets = {}
    # Init facets
    for facet in fod:
        facets[facet] = {'items': {}, 'items_total': 0}
    # Get facets from brains
    for brain in catalog_results:
        updateFacetsByBrain(facets, brain, fod)
    # transform items dict to list
    for facet in facets:
        facets[facet]['items'] = list(facets[facet]['items'].values())
    return facets


def getFacetsOptionsDict(facets, query):
    fod = {}
    groupby_criteria = getUtility(IGroupByCriteria).groupby
    for facet in facets:
        facet = facet.strip()
        if facet:
            opts = {}
            # Get options from GroupByCriteria utility
            if facet not in groupby_criteria:
                fod[facet] = {'msg': 'Facet not found'}
                continue

            idx = groupby_criteria[facet]['index']
            if not isinstance(query, list):
                opts['current_idx_value'] = safe_iterable(query.get(idx))
            else:
                # if query is a querybuilder dict
                opts['current_idx_value'] = safe_iterable(
                    [x['v'] for x in query if x['i'] == idx]
                )

            # Attribute name for getting filter value from brain
            opts['metadata_attr'] = groupby_criteria[facet]['metadata']
            # Optional modifier to set title from filter value
            opts['display_modifier'] = groupby_criteria[facet].get(
                'display_modifier', None)
            # CURRENTLY UNUSED: CSS modifier to set class on filter item
            #opts['css_modifier'] = groupby_criteria[facet].get('css_modifier', None)
            # Value blacklist
            value_blacklist = groupby_criteria[facet].get(
                'value_blacklist', None)
            # Allow value_blacklist to be callables for runtime-evaluation
            opts['value_blacklist'] = value_blacklist() if callable(value_blacklist) else value_blacklist  # noqa
            # CURRENTLY UNUSED: fallback to title sorted values
            #opts['sort_key_function'] = groupby_criteria[facet].get(
            #    'sort_key_function', lambda it: it['title'].lower())
            fod[facet] = opts
    return fod


def updateFacetsByBrain(facets, brain, options):
    for facet, opts in options.items():
        # Add facets with message (error, warning) only once
        if 'msg' in opts:
            if 'msg' not in facets[facet]:
                facets[facet]['msg'] = opts['msg']
            continue
        # Get values from brain and update facet
        # Get filter value
        val = getattr(brain, opts['metadata_attr'], None)
        if callable(val):
            val = val()
        # decode it to unicode
        val = safe_decode(val)
        # Make sure it's iterable, as it's the case for e.g. the subject index.
        val = safe_iterable(val)

        for filter_value in val:
            if filter_value is None or isinstance(filter_value, Missing):
                continue
            if opts['value_blacklist'] and filter_value in opts['value_blacklist']:  # noqa
                # Do not include blacklisted
                continue
            if filter_value in facets[facet]['items']:
                # Add counter, if filter value is already present
                facets[facet]['items'][filter_value]['total'] += 1
                continue

            # Set title from filter value with modifications,
            # e.g. uuid to title
            title = filter_value
            if filter_value is not '__EMPTY__' and callable(opts['display_modifier']):  # noqa
                sig = signature(opts['display_modifier'])
                if len(sig.parameters) == 1:
                    title = opts['display_modifier'](filter_value)
                else:
                    title = opts['display_modifier'](filter_value, facet)

                title = safe_decode(title)


            # Set selected state
            selected = filter_value in opts['current_idx_value']

            facets[facet]['items'][filter_value] = {
                'title': title,
                'value': filter_value,
                'total': 1,
                'selected': selected
            }
        facets[facet]['items_total'] =  len(facets[facet]['items'])


def getPossibleFacets():
    return list(facet for facet in getUtility(IGroupByCriteria).groupby)
