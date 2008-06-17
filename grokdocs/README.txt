grokdocs
********

Documentation for Grok.

What is `grokdocs`?
===================

It is merely a wrapper around the sphinx documentation engine. Sphinx
is also used to render current documentation of the Python programming
language.

Grokdocs generates HTML or LaTeX documents from the sources in the
Grok doc/ directory.


How to build documentation with `grokdocs`?
===========================================

`grokdocs` can easily be accessed by running:: 

   bin/grokdocs2html 

or::
	
   bin/grokdocs2latex

from the Grok root source directory. It will parse all the .rst files
in the doc/ directory of your local grok trunk.

The results, a readily rendered static HTML site or a bunch of LaTeX
files can be found afterwards by default in a newly created directory
called `build/html/` or `build/latex` respectively in the root of the
Grok source directory.

To generate PDF files, just change to <Grok-Root>/build/latex and run

   make

This should give you a tutorial, a reference and a grokdocs PDF
file, where the grokdocs.pdf includes all documents.

Note: to generate PDF files you need a complete LaTeX installation.


How to write Documentation
==========================

The Grok documentation held in the Grok SVN repository is limited to a
set of certain documents. If a document is maintained in the SVN, the
repository will be the authorative source, although it might be kept
on the grok.zope.org website as well. Any changes to the website
documents might be overriden when a new Grok release is published.

On the other hand, the Grok repository won't contain documents, for
which the website grok.zope.org is the authorative source. These
documents should be changed on the website itself.

What documents are handled by `grokdocs`?
-----------------------------------------

`grokdocs` takes only care for such documents, that have been agreed
to be maintained in the Grok subversion repository. This means it
cares for 

  - the Tutorial,

  - the Grok reference,

  - the 'developer notes'

and some minor documents.

These documents should only be changed in the subversion
repository. Any changes on the website will be overwritten by the
repository version, once a new release of Grok is done.

Any other documentation parts should be done on the grok.zope.org
website.

How to write Grok documents
---------------------------

The grokdocs engine is a wrapper around the sphinx engine developed by
Georg von Brandl for the general Python documentation.

See the `sphinx site <http://sphinx.pocoo.org/>`_ for details.

Sphinx uses ReStructuredText as document format. Furthermore it
provides many extensions to the standard ReSTructuredText directives,
so that you can markup special entities in a special way. This way you
can tell sphinx, that something is a class, a function, a parameter or
somthing else.

See the already existing documents to learn how to write documentation
with ReSTructuredText.
