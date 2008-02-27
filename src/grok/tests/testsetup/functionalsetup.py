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
=====================
Functional Test Setup
=====================

``FunctionalTestSetup`` helps to find and setup functional doctests
contained in a package. The most important method therefore might be
``getTestSuite()``, which searches a given package for doctest files
and returns all tests found as a suite of functional tests.

The work is done mainly in two stages:

1) The package is searched for appropriate docfiles, based on the
   settings of instcance attributes.

2) The tests contained in the found docfiles are setup as functional
   tests and added to a ``unittest.TestSuite`` instance.

There are plenty of default values active, if you use instances of
this class without further modifications. Therefore we will first
discuss the default behaviour and afterwards show, how you can modify
this behaviour to suit your special expectations on the tests.


Setting up a simple test suite
------------------------------

We want to register the tests contained in the local ``cave``
package. This has to be imported first, because we need the package as
a parameter for the testseupt constructor::

   >>> from grok.tests.testsetup import cave

Using the ``FunctionalTestSetup`` then is easy::

   >>> from grok.testing import FunctionalTestSetup
   >>> setup = FunctionalTestSetup(cave)
   >>> setup
   <grok.testing.FunctionalTestSetup object at 0x...>   

This setup is ready for use::

   >>> suite = setup.getTestSuite()
   >>> suite
   <unittest.TestSuite tests=[...]>

To sum it up, writing a test setup for a grok project now can be that
short::

   import unittest
   import grok
   import cave
   def test_suite():
       setup = grok.testing.FunctionalTestSetup(cave)
       return setup.getTestSuite()
   if __name__ == '__main__':
       unittest.main(default='test_suite')

This will find all .rst and .txt files in the package that provide a
certain signature (see below), register the contained tests as
functional tests and run them as part of a `unittest.TestSuite`.


FunctionalTestSetup default values
----------------------------------

Understanding the defaults is important, because the default values
are driving the whole process of finding and registering the test.


Which files are found by default?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basically, all files are accepted that

1) reside inside the package passed to the constructor. This includes
   subdirectories.

2) have a filename extension `.txt` or `.rst` (uppercase, lowercase
   etc. does not matter).

3) are *not* located inside a 'hidden' directory (i.e. a directory
   starting with a dot ('.'). Also subdirectories of 'hidden'
   directories are skipped.

4) contain a ReStructured Text meta-marker somewhere, that defines the
   file as a functional test explicitly::

       :Test-Layer: functional

   This means: there *must* be a line like the above one in the
   doctest file. The term might be preceeded or followed by whitspace
   characters (spaces, tabs).

Only files, that meet all four conditions are searched for functional
doctests. You can modify this behaviour of course, which will be
explained below in detail.


What options are set by default?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many options can be set, when registering functional doctests. When
using the default set of options, the following values are set::

* The setup-instance's ``setUp``-method is set as the ``setUp``
  function.

* The setup-instance's ``tearDown``-method is set as the ``tearDown``
  function.
  
     >>> setup.setUp
     <bound method FunctionalTestSetup.setUp of
      <grok.testing.FunctionalTestSetup object at 0x...>>

* The setup-instance's `globs` attribute is passed as the `globs`
  parameter. By default `globs` is a dictionary of functions, that
  should be'globally' available during testruns and it contains::

     >>> setup.globs
     {'http': <zope.app.testing.functional.HTTPCaller object at 0x...>,
      'sync': <function sync at 0x...>,
      'getRootFolder': <function getRootFolder at 0x...>}

  The functions `sync` and `getRootFolder` are provided by
  `zope.app.testing.functional`.

* The setup-instance's `optionsflags` attribute is passed. It
  includes by default the following doctest constants:

     >>> from zope.testing import doctest
     >>> setup.optionflags == (doctest.ELLIPSIS+
     ...                       doctest.NORMALIZE_WHITESPACE |
     ...                       doctest.REPORT_NDIFF)
     True

* Furthermore, additional keyword parameters are passed, which were
  set when calling the constructor. These keywords are stored in the
  setup object as `additional_options`. Those are empty by default::

     >>> setup.additional_options
     {}

Because functional tests require a ZCML layer, that defines a ZCML
setup for the tests, we provide a layer, that is driven by the file
`ftesting.zcml`, which comes with grok. The layer is accessible as the
setup instance attribute `layer`::

   >>> setup.layer
   <zope.app.testing.functional.ZCMLLayer instance at 0x...>

   >>> setup.layer.config_file
   '...ftesting.zcml'

   

No other options/parameters are set by default.


Customizing functional test setup:
----------------------------------

You can modify the behaviour of grok.testing.FunctionalTestSetup such,
that a different set of files is registered and/or the found tests are
registered with a different set of parameters/options. We will first
discuss modifying the set of files to be searched.


Customizing the doctest file search:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The searching of appropriate doctest files is basically done by the
base class `BasicTestSetup`. Its purpose is to determine the set of
files in a package, that contain functional tests. See the testfile
`basicsetup.py` to learn more about the procedure.

The functional test setup, however, provides a special
`isDocTestFile()` method, which does additional checking. Namely it
checks for the existance of the above mentioned ReStructured Text
meta-marker::

    `:Test-Layer: functional`

This is determined by a list of regular expressions, which is also
available as an object attribute::

    >>> setup.regexp_list
    ['^\\\\s*:(T|t)est-(L|l)ayer:\\\\s*(functional)\\\\s*']

This is the default value of functional test setups.

There are two files in the `cave` subpackage, which include that
marker. We can get the list of test files using
`getDocTestFiles()``::

    >>> testfile_list = setup.getDocTestFiles()
    >>> testfile_list.sort()
    >>> testfile_list
    ['...file1.txt', '...subdirfile.txt']

    >>> len(testfile_list)
    2

The ``isTestFile()`` method of our setup object did the filtering
here::

    >>> setup.isTestFile(testfile_list[0])
    True

The file file1.rst does not contain a functional test marker::

    >>> import os.path
    >>> path = os.path.join(os.path.dirname(cave.__file__),
    ...                     'test1.rst')
    >>> setup.isTestFile(path)
    False

The `regexp_list` attribute of a ``FunctionalTestSetup`` contains a
list of regular expressions, of which each one must at least match one
line of a searched file to be accepted. If you want to include files
with different marker-strings, just change this attribute. The value
will influence behaviour of the `isTestFile()``, ``getDocTestFiles()``
and ``getTestSuite()`` methods.

If you need more complex checks here, you can derive your customized
test setup class and overwrite ``isTestFile()``.

See `basicsetup.py` for further methods how to modify test file
search, for example by choosing another set of accepted filename
extensions.


Customizing the functional test setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To customize the setup of your tests, just modify the appropriate
attributes as explained before.

To setup a different setUp or tearDown function, you can define a
derived class, that overwrites these methods.

A convenient way to pass keyword parameters to the test setup, which
do not appear in the attributes, is passing these keywords (and the
values) to the constructor::

    >>> encoded_setup = FunctionalTestSetup(cave,
    ...                                     encoding='utf-8')

This will read all doctests 'utf-8' encoded, which allow umlauts and
similar chars in tests. Note, however, that you can archieve this very
special behaviour also by writing an appropriate encoding string in
the head of the doctest file.

All keywords passed to the constructor (except 'filter_func' and
'extensions') are also given to each individual test setup 'as-is'.

Alternatively you can also modify the `additional_options` dictionary
of a ``FunctionalTestSetup`` object.

    >>> encoded_setup.additional_options
    {'encoding': 'utf-8'}

    >>> encoded_setup.additional_options['encoding'] = 'latin1'



"""
