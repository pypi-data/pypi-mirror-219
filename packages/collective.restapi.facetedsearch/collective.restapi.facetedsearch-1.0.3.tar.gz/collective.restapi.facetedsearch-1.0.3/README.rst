.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

================================
collective.restapi.facetedsearch
================================

This addon provides Plone-REST-Api endpoints for a faceted search. The GET endpoint is highly inspired by the REST-Api search and the POST endpoint is highly inspired by the REST-Api querystringsearch. Configuration of facets must be done by overloading GroupByCriteria of collective.collectionfilter

Features
========

- GET endpoint ``@faceted-search`` can be used like the 'normal' search-endpoint of the REST-Api ``@search``, but it calculates and adds requested facets to the result set
- GET endpoint can list all available and configured facets
- POST endpoint ``@faceted-search`` can be used like the querystring search-endpoint of the REST-Api ``@querystring-search``, but it calculates and adds requested facets to the result set


Documentation
=============

GET endpoint
------------
``@faceted-search``

This endpoint accepts all parameter of the 'normal' search endpoint of the REST Api like ``b_size``, ``sort_on`` etc, and additionally three more: ``facets``, ``facets_only`` and ``possible_facets``.
To get a list of all available and configured facets add parameter ``possible_facets=1`` to the request.
Choose one or more of the available facets and add them as stringlist parameter  ``facets`` to the request. The search response json will be extended with object property "facets", and each of the facets contains a list with all item occurences of the facet in the resultset and the count how often they appear on the resultset


POST endpoint
-------------
``@faceted-search``

This endpoint accepts all parameter from the querystring-search endpoint of the REST Api, like ``query``, ``sort_on`` etc, and additionally three more: ``facets``, ``facets_only`` and ``possible_facets``. Provide the parameter in the request body as it is a post request.

Choose one or more of the available facets and add them as stringlist parameter  ``facets`` to the request.
The search response json will be extended with object property "facets", and each of the facets contains a list with all item occurences of the facet in the resultset and the count how often they appear on the resultset

Configuration of facets
-----------------------

Configuration is done by overloading collective.collectionfilter GroupByCriteria.
<https://github.com/collective/collective.collectionfilter#overloading-groupbycriteria>



Examples
========

GET Request
-----------

``http://localhost:8080/Plone/@faceted-search?b_size=24&SearchableText=Searchtext&facets=portal_type&facets=Subject``

POST Request
------------

``http://localhost:8080/Plone/@faceted-search`` with body::

  {
    "query": [

          {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.any",
            "v":
                ["stock", "person"]

        }
    ],
    "limit": 2000,
    "b_size": 2,
    "facets": [
        "tax_research_fields",
        "commentators",
        "location",
        "Subject"
    ]
  }


Installation
============


Install collective.restapi.facetedsearch by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.restapi.facetedsearch


and then running ``bin/buildout``


Dependencies
------------

All dependencies are installed automatically when installing collective.restapi.facetedsearch.
Here is just a list of those for reference:

- setuptools
- plone.restapi
- collective.collectionfilter


Contribute
==========

- Issue Tracker: https://github.com/collective/collective.restapi.facetedsearch/issues
- Source Code: https://github.com/collective/collective.restapi.facetedsearch.git
- Documentation: https://docs.plone.org


License
=======

The project is licensed under the GPLv2.
