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
===============
Unit Test Setup
===============

``UnitTestSetup`` helps to find and setup unit doctests contained in a
package. The most important method therefore might be
``getTestSuite()``, which searches a given package for doctest files
and returns all tests found as a suite of unit tests.

The work is done mainly in two stages:

1) The package is searched for appropriate docfiles, based on the
   settings of instcance attributes.

2) The tests contained in the found docfiles are setup as unit tests
   and added to a ``unittest.TestSuite`` instance.

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

Using the ``UnitTestSetup`` then is easy::

   >>> from grok.testing import UnitTestSetup
   >>> setup = UnitTestSetup(cave)
   >>> setup
   <grok.testing.UnitTestSetup object at 0x...>   

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
       setup = grok.testing.UnitTestSetup(cave)
       return setup.getTestSuite()
   if __name__ == '__main__':
       unittest.main(default='test_suite')

This will find all .rst and .txt files in the package that provide a
certain signature (see below), register the contained tests as unit
tests and run them as part of a `unittest.TestSuite`.


UnitTestSetup default values
----------------------------

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
   file as a unit test (and not: functional test) explicitly::

       :Test-Layer: unit

   This means: there *must* be a line like the above one in the
   doctest file. The term might be preceeded or followed by whitspace
   characters (spaces, tabs).

Only files, that meet all four conditions are searched for unit
doctests. You can modify this behaviour of course, which will be
explained below in detail.


What options are set by default?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many options can be set, when registering unit doctests. When using
the default set of options, the following values are set::

* The setup-instance's ``setUp``-method is set as the ``setUp``
  function.

* The setup-instance's ``tearDown``-method is set as the ``tearDown``
  function.
  
     >>> setup.setUp
     <bound method UnitTestSetup.setUp of
      <grok.testing.UnitTestSetup object at 0x...>>

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

No other options/parameters are set by default.


Customizing unit test setup:
----------------------------

You can modify the behaviour of grok.testing.UnitTestSetup such, that
a different set of files is registered and/or the found tests are
registered with a different set of parameters/options. We will first
discuss modifying the set of files to be searched.


Customizing the doctest file search:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The searching of appropriate doctest files is basically done by the
base class `BasicTestSetup`. Its purpose is to determine the set of
files in a package, that contain unit tests. See the testfile
`basicsetup.py` to learn more about the procedure.

The unit test setup, however, requires that files contain the above
mentioned ReStructured Text meta-marker::

    `:Test-Layer: unit`

This is determined by a list of regular expressions, which is also
available as an object attribute::

    >>> setup.regexp_list
    ['^\\\\s*:(T|t)est-(L|l)ayer:\\\\s*(unit)\\\\s*']

This is the default value of unit test setups.

There is one file in the `cave` subpackage, which includes that
marker. We can get the list of test files using
`getDocTestFiles()``::

    >>> testfile_list = setup.getDocTestFiles()
    >>> testfile_list
    ['...file1.rst']

    >>> len(testfile_list)
    1

The ``isTestFile()`` method of our setup object did the filtering
here::

    >>> setup.isTestFile(testfile_list[0])
    True

The file file1.txt does not contain a unit test marker::

    >>> import os.path
    >>> path = os.path.join(os.path.dirname(cave.__file__),
    ...                     'test1.txt')
    >>> setup.isTestFile(path)
    False

The `regexp_list` attribute of a ``UnitTestSetup`` contains a
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


Customizing the unit test setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To customize the setup of your tests, just modify the appropriate
attributes as explained before.

To setup a different setUp or tearDown function, you can define a
derived class, that overwrites these methods.

A convenient way to pass keyword parameters to the test setup, which
do not appear in the attributes, is passing these keywords (and the
values) to the constructor::

    >>> encoded_setup = UnitTestSetup(cave,
    ...                               encoding='utf-8')

This will read all doctests 'utf-8' encoded, which allow umlauts and
similar chars in tests. Note, however, that you can archieve this very
special behaviour also by writing an appropriate encoding string in
the head of the doctest file.

All keywords passed to the constructor (except 'filter_func' and
'extensions') are also given to each individual test setup 'as-is'.

Alternatively you can also modify the `additional_options` dictionary
of a ``UnitTestSetup`` object.

    >>> encoded_setup.additional_options
    {'encoding': 'utf-8'}

    >>> encoded_setup.additional_options['encoding'] = 'latin1'



"""
