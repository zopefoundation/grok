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


Generating the grok reference from grok source code
---------------------------------------------------

.. warning:: This is work-in-progress and may lead to disappointing
             results.

The script mkgrokref.py is able to generate the sources for grok
reference from the grok source code. It must be run with the
appropriate PYTHONPATH set (i.e.: including the grok package to scan,
all packages required by grok, namely the zope 3 packages, and the
python standard packages). See the header of the script for further
documentation. There are currently no commandline options supported by
mkgrokref.py.

To get a very plain reference::

  $ python2.4 mkgrokref.py > myreference.txt

This will produce a ReST formatted text file. Go on with::

  $ rst2latex myreference.txt myreference.tex

Transform the ReStructucturedText to LaTeX. Now we got a LaTeX source,
which can be further processed as described above. For example::

  $ mkhowto --pdf myreference.tex

The rst2latex script is part of the python docutils package.

