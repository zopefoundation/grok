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


How can I run `grokdocs`?
=========================

`grokdocs` can be accessed by running 

	bin/grokdocs2html 

or
	
	bin/grokdocs2latex

from the Grok root source directory.

The results can be found by default in a newly created directory
called `build` in the root of the Grok source directory.

To generate PDF files, just change to <Grok-Root>/build/latex and run

   make

This should give you a tutorial, a reference and a grokdocs PDF file.

You need LaTeX installed, to run pdflatex.


What documents are handled by `grokdocs`?
=========================================

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
