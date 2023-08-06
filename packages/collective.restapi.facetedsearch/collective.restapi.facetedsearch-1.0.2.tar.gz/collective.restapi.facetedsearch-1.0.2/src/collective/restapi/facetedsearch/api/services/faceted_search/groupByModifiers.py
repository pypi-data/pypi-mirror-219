# -*- coding: utf-8 -*-
from collective.collectionfilter.interfaces import IGroupByCriteria
from collective.collectionfilter.interfaces import IGroupByModifier
from zope.component import adapter
from zope.interface import implementer
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from collective.taxonomy.interfaces import ITaxonomy
from plone.api import portal

# see also collective.collectionfilter 'Overloading GroupByCriteria' how to set display_modifier function for indexes or assign a metadata column name different to the index name
@implementer(IGroupByModifier)
@adapter(IGroupByCriteria)
def groupby_modifier(groupby):
    pass
