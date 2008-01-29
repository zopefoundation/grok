##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
================
Basic Test Setup
================

``BasicTestSetup`` is a class to support easier setup of tests in grok
projects. It acts merely as a container for shared functions, methods
and attributes needed by 'real' test setups which are derived from
it. Itself provides *no* ``getTestSuite()`` method, which is needed to
setup real tests.

A ``BasicTestSetup`` tries to find all doctest files defined in a given
package. See `functionalsetup.py` for setting up real functional tests
and `unittestsetup.py` for 'real' setup of unittests.

For a general introduction into testing with grok see the appropriate
howto on the grok homepage.

The TestSetup classes all search and handle doctest files.

All we need to setup a testsuite, is the package to search::

   >>> from grok.tests.testsetup import cave
   >>> from grok.testing import BasicTestSetup
   >>> basic_setup = BasicTestSetup(cave)
   >>> basic_setup
   <grok.testing.BasicTestSetup object at 0x...>

The package is stored as an instance-attribute::

   >>> basic_setup.package
   <module 'grok.tests.testsetup.cave' from ...>

The ``BasicTestSetup`` serves merely as a container for attributes and
methods needed by derived classes, that provide proper test setup.

One of it's resposibilities is, to find doctest files, which is done
by the ``getDocTestFiles()`` method. If we run this method, we
get a list of filenames::

   >>> file_list = basic_setup.getDocTestFiles()
   >>> len(file_list)
   4

The filenames are all absolute::

   >>> import os.path
   >>> [x for x in file_list if not os.path.isabs(file_list[0])]
   []


Which files are found?
----------------------

By default, all .txt and .rst files are taken
into account::

   >>> exts = ['.rst', '.txt']
   >>> [x for x in file_list if not os.path.splitext(x)[1].lower() in exts]
   []

All forms of an extension are found, regardless of whether they are
uppercase, lowercase or mixed-case::

   >>> file_list
   [...'...file2.TXT'...]

Also subdirectories are searched::

   >>> file_list
   [...'...subdirfile.txt'...]

Hidden directories, however, are skipped. To check this, we look for a
'hidden' testfile put into a hidden directory in the `cave`
directory. We first make sure, that the hidden file really exists::

   >>> cavepath = os.path.dirname(cave.__file__)
   >>> hiddenpath = os.path.join(cavepath, '.hiddendir', 'hiddenfile.txt')
   >>> os.path.exists(hiddenpath)
   True

And now check that it was *not* included in the file list::

   >>> hiddenpath in file_list
   False

To provide a more finegrained filtering, ``BasicTestSetup`` provides a
method ``isTestFile(filepath)``, which returns ``True`` for accepted
files and ``False`` otherwise. This method is called for every file
found by ``getDoctesFiles``. By default it only filters files by their
filename extension and compares it with the instance-attribute
``extensions``, which by default is the list ``['.rst', '.txt']``::

   >>> basic_setup.extensions
   ['.rst', '.txt']

   >>> basic_setup.isTestFile('')
   False

   >>> basic_setup.isTestFile('cave.txt')
   True

   >>> basic_setup.isTestFile('cave.rst')
   True

   >>> basic_setup.isTestFile('cave.RsT')
   True

   >>> basic_setup.isTestFile('cave.foo')
   False


How to find a customized set of files:
--------------------------------------

There are several possibilities to modify the search results of
``getDocTestFiles()``. If it is only a matter of filename extension,
the instance's attribute ``extensions`` can be modified::

   >>> basic_setup.extensions = ['.foo']
   >>> basic_setup.getDocTestFiles()
   ['...notatest1.foo']

If things need a more complex filtering, you can also redefine the
filter function, which by default is the ``isTestFile()`` function as
mentioned above.

You can pass an alternative filterfunction as keyword parameter
``filter_func`` to the ``BasicTestSetup`` constructor::

   >>> def myFilter(filename):
   ...     return filename.endswith('.txt')
   >>> basic_setup2 = BasicTestSetup(cave, filter_func=myFilter)
   >>> len(basic_setup2.getDocTestFiles())
   2

Note, that the filter function must accept a single parameter, which
should contain a filepath as string and it should return a boolean
value to indicate, whether the file given by the filepath should be
included in the test suite or not.

A different set of accepted filename extensions can also be passed to
the constructor, using the ``extensions`` keyword::

   >>> basic_setup3 = BasicTestSetup(cave, extensions=['.txt'])

Note, that the extensions should alway be written with a leading dot
and in lower case. Such we can find only .txt files::

   >>> len(basic_setup3.getDocTestFiles())
   3

Now also the .TXT file was found, which was omitted in the test
before.

The set of directories, which are accepted as doctest containers, is
defined by the ``isTestDirectory`` method, which by default only skips
'hidden' directories, i.e. directories, that start with a dot ('.').

   >>> basic_setup3.isTestDirectory('foo/bar/somdir')
   True

   >>> basic_setup3.isTestDirectory('foo/bar/.hiddendir')
   False

You can change this behaviour by deriving your own setup class and
overwriting the method. This works also with derived classes like
``FunctionalTestSetup``.


Find terms in docfiles:
-----------------------

For convenience ``BasicTestSetup`` provides a method ``fileContains``,
which parses the contents of a file to match a list of regular
expressions. If every of the regular expressions in the list matched
at least one line of the file, ``True`` is returned, ``False``
otherwise.

``fileContains`` is a helper function to search files for certain
terms and expressions. It is implemented as a method (instead a
standalone function), to enable developers to replace it with a more
complex implementation that also accesses other instance attributes
like the package or similar.

File paths, that cannot be found, are silently ignored::

   >>> basic_setup4 = BasicTestSetup(cave, extensions=['.foo'])
   >>> basic_setup4.fileContains('blah', ['FOO'])
   False

We pick up an existing file path::

   >>> file_list = basic_setup4.getDocTestFiles()
   >>> len(file_list)
   1

   >>> filepath = file_list[0]
   >>> filepath.endswith('notatest1.foo')
   True

This file contains a string 'ME GROK SMASH ZCML!!', which we can
search for::

   >>> basic_setup4.fileContains(filepath, ['ME GROK'])
   True

   >>> basic_setup4.fileContains(filepath, ['ME GROK IS DUMB'])
   False

The terms to search are handled as real regular expressions as
provided by the ``re`` package::

   >>> basic_setup4.fileContains(filepath, ['^ME (G|g)ROK.*'])
   True

We can also search for several matches::

   >>> basic_setup4.fileContains(filepath, ['.*SMASH.*', '.*GROK.*'])
   True

If one of the searched terms is not found, the whole thing fails::

   >>> basic_setup4.fileContains(filepath, ['.*DUMB.*', '.*GROK.*'])
   False

It does not matter, whether matches occur in the same line or in
different ones. In the example file there is also a heading stating
'This is not a test'. Let's check this::

   >>> basic_setup4.fileContains(filepath, ['ME GROK', 'This is not'])
   True


Note: The evaluation of regular expressions is done without any
modifiers. Namely the matching is case sensitive::

   >>> basic_setup4.fileContains(filepath, ['me grok'])
   False

Furthermore, matches are only done against one line at a time.



"""
