=========================
The grok reference manual
=========================

NOTE: The Grok reference manual is in the process of being migrated to a
RestructuredText infrastructure.

How to build HTML documentation from ReST files
-----------------------------------------------

The toolchain to generate HTML from the ReST files in this directory
is currently also under construction.

A current snapshot of the toolchain can be retrieved from the
jasper-docgroktools branch of the grok svn repository.

   $ svn co http://svn.zope.org/grok/branches/jasper-grokdoctool \
               grokdoctool

Then change into the checked out directory::

   $ cd grokdoctool

and follow the advices given in README.txt.

Note, that you need development files for libxml2 and libxslt to
install lxml correctly. Debian/Ubuntu users can get the correct files,
using

   $ apt-get install libxml2-dev libxslt-dev

After generating the grokdoctool, you can run it with the source
directory of the restructured text files as argument:

   $ bin/grokdoctool <path-to-the-rest-files-dir>

This procedure is subject to changes. The format of the reference
documentation (ReST) is not.
