=========================
The grok reference manual
=========================

The manual is written using LaTeX with support for the Python documentation
markup. The tex sources can be compiled to HTML and PDF. To build the manual,
you need the 'mkhowto' script from a recent Python source distribution.

Build the HTML
--------------

Compiling the sources into HTML::

  $ mkhowto --html reference.tex

The directory 'reference/' keeps all files required to display the manual after
that call and can be put on a static webserver.

Build the PDF
-------------

The file 'reference.pdf' will contain the PDF version of the manual after this
call::

  $ mkhowto --pdf reference.tex

Installing prerequisites on Debian and Ubuntu systems
-----------------------------------------------------

On recent Debian and Ubuntu systems, the following packages provide the
required toolset for compiling the sources.

The basic LaTeX infrastructure::

  $ sudo apt-get install tetex-base tetex-bin tetex-extra latex2html

The python-dev package provides the mkhowto script::

  $ sudo apt-get install python2.4-dev

This script will be located in::

  /usr/lib/python2.4/doc/tools/mkhowto
