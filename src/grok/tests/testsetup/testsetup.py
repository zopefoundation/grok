##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
Tests for testsetups in grok.testing
************************************

The grok testing support provides a z3c.testsetup which should suit
most grokprojects. Main parts of this support are

- a grok.testing.register_all_tests() function that registers all
  marked tests found in a package and

- a TestGetter, that is reusable in own projects.

We will discuss both in the following sections.

grok.testing.register_all_tests(<pkg>)
======================================

A function that requires a package and delivers a callable which, if
called without arguments, returns a test suite with all tests of all
doctestfiles (functional *and* unit doctests) and Python tests found
in the given package.

With this function you can setup tests like this::

   import grok
   test_suite = grok.testing.register_all_tests('cave')

In standard grokprojects, this should find all files and modules, that
have a .txt or .rst filename extension (doctests) or are regular
Python modules (Python tests). Only those tests are found, that
provide a certain marker string (see below).

To modify the default values (described below), you can pass
(optional) keyword parameters. The complete syntax is::

   grok.testing.register_all_tests(
      <pkg_or_dotted_name>,
      filter_func = <function>,
      ffilter_func = <function>,
      ufilter_func = <function>,
      pfilter_func = <function>,
      extensions = <list_of_filename_extenstions>,
      fextensions = <list_of_filename_extenstions>,
      uextensions = <list_of_filename_extenstions>,
      encoding = <string_with_encoding_specifier>,
      checker = <output_checker>,
      globs = <dict_of_globals>,
      fglobs = <dict_of_globals>,
      uglobs = <dict_of_globals>,
      setup = <function>,
      fsetup = <function>,
      usetup = <function>,
      teardown = <function>,
      fteardown = <function>,
      uteardown = <function>,
      optionflags = <optionflags>,
      foptionflags = <optionflags>,
      uoptionflags = <optionflags>,
      zcml_config = <path_to_zcml_config_file>,
      layer_name = <string>,
      layer = <complete_zcml_layer>)

where all parameters (except the first one) are optional. Those
options that are preceeded by 'u', 'f', or 'p' affect only unit
doctests, functional doctests or Python tests respectively.

The work of the function is done in two steps:

1) Doctestfiles and Python modules with tests are collected and

2) the tests contained in them are registered with the given values or
   default values.

We will discuss the default values and how to modify the behaviour of
both steps.


A simple test setup with register_all_tests()
---------------------------------------------

The `register_all_tests()` function must be called with a package as
first argument. This package can be given in 'dotted name' notation::

   >>> import grok
   >>> setup = grok.testing.register_all_tests(
   ...             'grok.tests.testsetup.cave')
   >>> setup
   <grok.testing.GrokTestCollector object at 0x...>

Alternatively, we can pass the 'real' package, which requires to
import it before::

   >>> from grok.tests.testsetup import cave
   >>> setup = grok.testing.register_all_tests(cave)
   >>> setup
   <grok.testing.GrokTestCollector object at 0x...>

In both cases we get a `GrokTestCollector` which is a callable, that
returns a ``unittest.TestSuite`` upon being called::

   >>> suite = setup()
   >>> suite
   <unittest.TestSuite tests=[...]>

We import a function of the z3c.testsetup to list the set of included
testfiles/modules::

   >>> from z3c.testsetup.tests.test_testsetup import get_basenames_from_suite
   >>> get_basenames_from_suite(suite)
   ['file1.py', 'file1.rst', 'file1.txt', 'subdirfile.txt']
   
These are files/modules located in the ``cave`` package. If you look
into these files, you will see, that `file1.py` is a normal Pyhton
testmodule, `file1.rst` contains unitdoctests and both .txt-files
are functional doctest files.

There are some more files in the `cave` package, which also contain
tests. Why haven't they been found? A doctestfile or module must meet
certain requirements to be accepted.


Which files/modules are found by default?
-----------------------------------------

Basically, all files/modules are found that

1) reside inside the package passed to the function. This includes
   subdirectories/subpackages.

2) have a filename extension `.txt` or `.rst` (uppercase, lowercase
   etc. does not matter) if they should be registered as unit or
   functional doctests. Python tests are always looked up in regular
   Python modules.

3) are *not* located inside a 'hidden' directory (i.e. a directory
   starting with a dot ('.'). Also subdirectories of 'hidden'
   directories are skipped. Python tests are only found, if the
   subpackage they are in is a real subpackage (the directory itself
   and all parent directories inside the root package must have an
   `__init__.py`).

4) contain a ReStructured Text meta-marker somewhere, that defines the
   file as a functional or unit doctest or Python test explicitly.

   For functional doctests, the file must contain::
   
       :Test-Layer: functional

   For unit doctests the file must contain::

       :Test-Layer: functional

   Python test modules must provide a module docstring that contains::

       :Test-Layer: python

   This means: there *must* be a line like the above one in the
   doctest file or python modules. The terms might be preceeded or
   followed by whitspace characters (spaces, tabs).

All this is the default behaviour.


Customize the set of files/modules found
----------------------------------------

If we want to grab a different set of doctest files and/or modules, we
can use three options:

1) Pass an `extensions` parameter (doctests only):

     This by default is the list ``['.txt', '.rst']. If we want to
     search .foo files too, then we can do it like this::

        >>> setup = grok.testing.register_all_tests(
        ...     cave, extensions=['.foo'])

     Note, that the behaviour is not cummulative. We have to give the
     complete list. This will result in a different set of files
     found::

        >>> suite = setup()
        >>> get_basenames_from_suite(suite)
        ['file1.py', 'notatest1.foo', 'notatest1.foo']

     This result may look surprisingly, but is correct. The `file1.py`
     module was included, because Python tests are not affected by the
     `extensions` option and `file1.py` is a Python test. The
     `notatest1.foo` file appears twice, because it was once
     registered as a unit test and once as a functional test (yes,
     this is possible although it might not make too much sense in
     reality).

     To modify only the selection of functional doctests, you can pass
     the `fextensions` option::

        >>> setup = grok.testing.register_all_tests(
        ...     cave, fextensions=['.foo'])

     Now .txt and .rst files will be searched for unit doctests and
     .foo files for functional doctests::

        >>> suite = setup()
        >>> get_basenames_from_suite(suite)
        ['file1.py', 'file1.rst', 'notatest1.foo']

     If we provide an `<x>extensions` parameter and an `extensions`
     parameter, the more specific one will override the more general
     one. If for example we use::

        >>> setup = grok.testing.register_all_tests(
        ...     cave, extensions=['.foo'], fextensions=['.txt'])

     then all unitdoctests with filename extension .foo will be found
     and all functional doctests in .txt files::

        >>> suite=setup()
        >>> get_basenames_from_suite(suite)
        ['file1.py', 'file1.txt', 'notatest1.foo', 'subdirfile.txt']

     Python tests are not affected by the `extensions` parameter. But
     to be clear: you can search for doctests (and find them!) in
     Python files. See `Doctests in Python modules`_ below.
     

Doctests in Python modules
--------------------------

or: what the heck are Python tests after all?

That a file with tests is a Python module, does not mean
automatically, that it is a Python test in the sense of
z3c.testsetup. Instead many packages contain Python files, that
contain **doctests** and not real Python tests. The file you are
reading is an example for such a module with doctests.






"""
