grokdoctool - Grok's ReST 2 HTML convertor
=========================================

version: 0.1 (SVN/Unreleased)

This package contains a tool (and some test data) to convert Grok's ReST
documentation (reference documentation) to HTML for the Grok website
(http://grok.zope.org). The code is partially copied from the Python core
documentation generation tools, modified to generate ReST rather than Latex.

The tool walks through a directory passed in as an argument (defaulting to the
current working directory) to find .rst or .txt files, then, for each of the
files found, uses docutils to convert ReST to XML, and after that XSLT (lxml)
to convert the XML to HTML. Optionally it will allow you to specify what
stylesheet to use (to allow using it for other projects besides Grok).

Installation
============

The package provides a setuptools script, called 'setup.py', which can install
the application. To perform an installation, first run 'python setup.py build'
as a normal user, then 'python setup.py install' as root (sudo). Note that the
Python interpreter used to run setup.py will be the one used for running the
tool (tested with Python 2.5 and docutils 4.x).

After installation, a script called 'grokdoctool' will be in one of your 'bin'
directories (using the --prefix location with which the Python executable was
built, so if Python was installed in /usr/local, the script will be placed in
/usr/local/bin).

Using the script
================

Using the script is straight-forward, just call::

  $ grokdoctool <mydir>

to convert all the files with a .rst or .txt extension in <mydir> to HTML.

For an overview of the available options, run::

  $ grokdoctool --help

Questions, remarks, etc.
========================

For questions, remarks, bug reports, patches, etc. send an email to either
jasper@infrae.com or guido@pragmagik.com.

