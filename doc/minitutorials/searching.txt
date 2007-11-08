===============
Search Tutorial
===============

:Author: Sebastian Ware

Introduction
------------
Grok supports the vanilla indexing services available in Zope 3 straight out of
the box. Catalog uses developer defined indexes for searching. In other words,
you have to define the indexes you want to use to search you objects before you
perform the actual search.

* FieldIndex: search matching an entire field
* SetIndex: search for keywords in a field
* TextIndex: full-text searching
* ValueSearch: search for values using ranges

The time for Zope to generate a new index is proportional to the amount of
objects that need to be analysed.

Setup
-----
The egg (package) containing the search functionality is called
[zc.catalog-x.x.x-py2.x.egg] and is installed when "buildout.cfg" contains
"zope.app.catalog" in the list of the directive "zcml=". This is the default
configuration.

Some applications might require specific versions of catalog. This is specified
in the "setup.py" script. The following directive indicates that zc.catalog
version 1.1.1 is required.

.. code-block:: python

    install_requires=['setuptools',
                  'grok',
                  'zc.catalog==1.1.1',
                  'hurry.query',
                  'hurry.workflow',
                  ],

The "hurry.query" package gives you some simple tools to perform advanced
searching. (add "hurry.query" to "zcml=" in "buildout.cfg")

Example
-------

.. code-block:: python

    # interfaces.py
    class IProtonObject(Interface):
        """
        This is an interface to the class who's objects I want to index.
        """
        body = schema.Text(title=u'Body', required=False)

.. code-block:: python

    # protonobject.py
    class ProtonObject(grok.Model):
        """
        This is the actual class.
        """
        interface.implements(interfaces.IProtonObject)

        def __init__(self, body):
            self.body = body

.. code-block:: python

    # app.py
    from hurry.query.query import Query, Text
    # hurry.query is a simplified search query language that
    # allows you to create ANDs and ORs.

    class ContentIndexes(grok.Indexes):
        """
        This is where I setup my indexes. I have two indexes;
        one full-text index called "text_body",
        one field index called "body".
        """
        grok.site(ProtonCMS)

        grok.context(interfaces.IProtonObject)
        # grok.context() tells Grok that objects implementing
        # the interface IProtonObject should be indexed.

        grok.name('proton_catalog')
        # grok.name() tells Grok what to call the catalog.
        # if you have named the catalog anything but "catalog"
        # you need to specify the name of the catalog in your
        # queries.

        text_body = index.Text(attribute='body')
        body = index.Field(attribute='body')
        # The attribute='body' parameter is actually unnecessary if the attribute to
        # be indexed has the same name as the index.

    class Index(grok.View):
        grok.context(ProtonCMS)

        def search_content(self, search_query):
                # The following query does a search on the field index "body".
                # It will return a list of object where the entire content of the body attribute
                # matches the search term exactly. I.e. search_query == body
                result_a = Query().searchResults(
                                   query.Eq(('proton_catalog', 'body'), search_query)
                                   )

                # The following query does a search on the full-text index "text_body".
                # It will return objects that match the search_query. You can use wildcards and
                # boolean operators.
                #
                # Examples:
                # "grok AND zope" returns objects where "body" contains the words "grok" and "zope"
                # "grok or dev*" returns objects where "body" contains the word "grok" or any word
                # beginning with "dev"
                result_b = Query().searchResults(
                                   Text( ('proton_catalog', 'text_body'), search_query)
                                   )

                return result_a, result_b

Note
----
In the above example, the indexes are only added when a new application is
installed. You will have to manually create new indexes if you wish to add them
to an existing application.

Learning More
-------------
The "hurry.query" package contains the DocTest "query.txt" that shows how to
perform more complex search queries.
