# -*- coding: utf-8 -*-
from .handler import FacetedSearchHandler, FacetedQuerystringSearchHandler
from plone.restapi.search.utils import unflatten_dotted_dict
from plone.restapi.services import Service


class FacetedSearchGet(Service):
    def reply(self):
        query = self.request.form.copy()
        query = unflatten_dotted_dict(query)
        return FacetedSearchHandler(self.context, self.request).search(query)


class FacetedSearchPost(Service):
    def reply(self):
        return FacetedQuerystringSearchHandler(self.context, self.request).search()
