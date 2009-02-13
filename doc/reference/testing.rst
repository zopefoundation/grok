*******
Testing
*******

Installing the testing tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every Grok-based project will install a test runner that can find
and run all test cases for your project. This test runner is installed
using Buildout with the 
`zc.recipe.testrunner <http://pypi.python.org/pypi/zc.recipe.testrunner>`_
recipe. The default configuration is::

    [test]
    recipe = zc.recipe.testrunner
    eggs = <my-grok-project-name>
    defaults = ['--tests-pattern', '^f?tests$', '-v']

Using the test runner
~~~~~~~~~~~~~~~~~~~~~

The test runner can be invoked by the `test` program in your projects
`bin` directory.

usage
=====

  Usage: test [options] [MODULE] [TEST]

options: help
=============

  -h, --help
    show this help message and exit

options: searching and filtering
================================

    options in this group are used to define which tests to run.

    -s PACKAGE, --package=PACKAGE, --dir=PACKAGE
        Search the given package's directories for tests.
        This can be specified more than once to run tests in
        multiple parts of the source tree.  For example, if
        refactoring interfaces, you don't want to see the way
        you have broken setups for tests in other packages.
        You *just* want to run the interface tests.  Packages
        are supplied as dotted names.  For compatibility with
        the old test runner, forward and backward slashed in
        package names are converted to dots.  (In the special
        case of packages spread over multiple directories,
        only directories within the test search path are
        searched. See the --path option.)
    -m MODULE, --module=MODULE
        Specify a test-module filter as a regular expression.
        This is a case-sensitive regular expression, used in
        search (not match) mode, to limit which test modules
        are searched for tests.  The regular expressions are
        checked against dotted module names.  In an extension
        of Python regexp notation, a leading "!" is stripped
        and causes the sense of the remaining regexp to be
        negated (so "!bc" matches any string that does not
        match "bc", and vice versa).  The option can be
        specified multiple test-module filters.  Test modules
        matching any of the test filters are searched.  If no
        test-module filter is specified, then all test modules
        are used.
    -t TEST, --test=TEST
        Specify a test filter as a regular expression.  This
        is a case-sensitive regular expression, used in search
        (not match) mode, to limit which tests are run.  In an
        extension of Python regexp notation, a leading "!" is
        stripped and causes the sense of the remaining regexp
        to be negated (so "!bc" matches any string that does
        not match "bc", and vice versa).  The option can be
        specified multiple test filters. Tests matching any of
        the test filters are included.  If no test filter is
        specified, then all tests are run.
    -u, --unit
        Run only unit tests, ignoring any layer options.
    -f, --non-unit
        Run tests other than unit tests.
    --layer=LAYER
        Specify a test layer to run.  The option can be given
        multiple times to specify more than one layer.  If not
        specified, all layers are run. It is common for the
        running script to provide default values for this
        option.  Layers are specified regular expressions,
        used in search mode, for dotted names of objects that
        define a layer.  In an extension of Python regexp
        notation, a leading "!" is stripped and causes the
        sense of the remaining regexp to be negated (so "!bc"
        matches any string that does not match "bc", and vice
        versa).  The layer named 'unit' is reserved for unit
        tests, however, take note of the --unit and non-unit
        options.
    -a AT_LEVEL, --at-level=AT_LEVEL
        Run the tests at the given level.  Any test at a level
        at or below this is run, any test at a level above
        this is not run.  Level 0 runs all tests.
    --all
        Run tests at all levels.
    --list-tests
        List all tests that matched your filters.  Do not run
        any tests.

options: reporting
==================

    Reporting options control basic aspects of test-runner output

    -v, --verbose
        Make output more verbose. Increment the verbosity
        level.
    -q, --quiet
        Make the output minimal, overriding any verbosity
        options.
    -p, --progress
        Output progress status
    --no-progress
        Do not output progress status.  This is the default,
        but can be used to counter a previous use of --progress or -p.
    --auto-progress
        Output progress status, but only when stdout is a terminal.
    -c, --color
        Colorize the output.
    -C, --no-color
        Do not colorize the output.  This is the default, but
        can be used to counter a previous use of --color or -c.
    --auto-color
        Colorize the output, but only when stdout is a terminal.
    --slow-test=N
        With -c and -vvv, highlight tests that take longer
        than N seconds (default: 10).
    -1, --hide-secondary-failures
        Report only the first failure in a doctest. (Examples
        after the failure are still executed, in case they do
        any cleanup.)
    --show-secondary-failures
        Report all failures in a doctest.  This is the
        default, but can be used to counter a default use of
        -1 or --hide-secondary-failures.
    --ndiff
        When there is a doctest failure, show it as a diff
        using the ndiff.py utility.
    --udiff
        When there is a doctest failure, show it as a unified diff.
    --cdiff
        When there is a doctest failure, show it as a context diff.

options: analysis
=================

    Analysis options provide tools for analysing test output.

    -D, --post-mortem
        Enable post-mortem debugging of test failures
    -g GC, --gc=GC
        Set the garbage collector generation threshold.  This
        can be used to stress memory and gc correctness.  Some
        crashes are only reproducible when the threshold is
        set to 1 (aggressive garbage collection).  Do "--gc 0"
        to disable garbage collection altogether.  The --gc
        option can be used up to 3 times to specify up to 3 of
        the 3 Python gc_threshold settings.
    -G GC_OPTION, --gc-option=GC_OPTION
        Set a Python gc-module debug flag.  This option can be
        used more than once to set multiple flags.
    -N REPEAT, --repeat=REPEAT
        Repeat the tests the given number of times.  This
        option is used to make sure that tests leave their
        environment in the state they found it and, with the
        --report-refcounts option to look for memory leaks.
    -r, --report-refcounts
        After each run of the tests, output a report
        summarizing changes in refcounts by object type.  This
        option that requires that Python was built with the
        --with-pydebug option to configure.
    --coverage=COVERAGE
        Perform code-coverage analysis, saving trace data to
        the directory with the given name.  A code coverage
        summary is printed to standard out.
    --profile=PROFILE
        Run the tests under cProfiler or hotshot and display
        the top 50 stats, sorted by cumulative time and number
        of calls.
    --pychecker
        Run the tests under pychecker

options: setup
==============

    Setup options are normally supplied by the testrunner script, although
    they can be overridden by users.

    --path=PATH
        Specify a path to be added to Python's search path.
        This option can be used multiple times to specify
        multiple search paths.  The path is usually specified
        by the test-runner script itself, rather than by users
        of the script, although it can be overridden by users.
        Only tests found in the path will be run.  This option
        also specifies directories to be searched for tests.
        See the search_directory.
    --test-path=TEST_PATH
        Specify a path to be searched for tests, but not added
        to the Python search path.  This option can be used
        multiple times to specify multiple search paths.  The
        path is usually specified by the test-runner script
        itself, rather than by users of the script, although
        it can be overridden by users.  Only tests found in
        the path will be run.
    --package-path=PACKAGE_PATH
        Specify a path to be searched for tests, but not added
        to the Python search path.  Also specify a package for
        files found in this path. This is used to deal with
        directories that are stitched into packages that are
        not otherwise searched for tests.  This option takes 2
        arguments.  The first is a path name. The second is
        the package name.  This option can be used multiple
        times to specify multiple search paths.  The path is
        usually specified by the test-runner script itself,
        rather than by users of the script, although it can be
        overridden by users.  Only tests found in the path
        will be run.
    --tests-pattern=TESTS_PATTERN
        The test runner looks for modules containing tests.
        It uses this pattern to identify these modules.  The
        modules may be either packages or python files.  If a
        test module is a package, it uses the value given by
        the test-file-pattern to identify python files within
        the package containing tests.
    --suite-name=SUITE_NAME
        Specify the name of the object in each test_module
        that contains the module's test suite.
    --test-file-pattern=TEST_FILE_PATTERN
        Specify a pattern for identifying python files within
        a tests package. See the documentation for the
        --tests-pattern option.
    --ignore_dir=IGNORE_DIR
        Specifies the name of a directory to ignore when
        looking for tests.

options: other
==============

    Other options

    -k, --keepbytecode
        Normally, the test runner scans the test paths and the
        test directories looking for and deleting pyc or pyo
        files without corresponding py files.  This is to
        prevent spurious test failures due to finding compiled
        modules where source modules have been deleted. This
        scan can be time consuming.  Using this option
        disables this scan.  If you know you haven't removed
        any modules since last running the tests, can make the
        test run go much faster.
    --usecompiled
        Normally, a package must contain an __init__.py file,
        and only .py files can contain test code.  When this
        option is specified, compiled Python files (.pyc and
        .pyo) can be used instead:  a directory containing
        __init__.pyc or __init__.pyo is also considered to be
        a package, and if file XYZ.py contains tests but is
        absent while XYZ.pyc or XYZ.pyo exists then the
        compiled files will be used.  This is necessary when
        running tests against a tree where the .py files have
        been removed after compilation to .pyc/.pyo.  Use of
        this option implies --keepbytecode.
    --exit-with-status
        Return an error exit status if the tests failed.  This
        can be useful for an invoking process that wants to
        monitor the result of a test run.

Discovering Test Cases
~~~~~~~~~~~~~~~~~~~~~~

The test runner looks for modules containing tests. It uses the default
pattern of \'^f?tests$\' to identify these modules. The test runner will
then use the name `test_suite` in all matching modules as the object to
provide test suites.

To make it easier to automatically discover tests and group them into
different test suites, Grok provides a function for registering all
tests.

Automatic test detection and setup supports three kinds of tests:

    * **python tests:** Python modules which contain
      ``unittest.TestCase`` classes.

    * **unit doctests:** plain-text files that are written as doctests,
      but require no complicated layer setup.

    * **functional doctests:** plain-text files that are written as doctests,
      but also require the full Zope 3/Grok framework to test for example
      browser requests.


:func:`grok.testing.register_all_tests` -- automatically find all test cases
============================================================================

.. function:: grok.testing.register_all_tests(package_name, *args, **kw)

    Get all functional, unit and python tests specified in the package
    name and return them as a test suite.
    
    Positional and keyword arguments will be passed to the TestSetups only
    if they are appropriate to the individual TestSetups. The keyword 
    parameters are:

    `filter_func`
    
    A function that takes an absolute filepath and retur    - (.*)ns `True` or
    `False`, depending on whether the file should be included in the
    test suite as doctest or not. `filter_func` applies only to
    doctests.
    
    `extensions`

    A list of filename extensions to be considered during test
    search. Default value is `['.txt', '.rst']`. Python tests are not
    touched by this (they have to be regular Python modules with '.py'
    extension).
    
    `encoding`
    
    The encoding of testfiles. 'utf-8' by default. Setting this to `None`
    means using the default value.
    
    `checker`
    
    An output checker for functional doctests.
    
    `globs`
    
    A dictionary of things that should be available immediately
    (without imports) during tests. Defaults are:

    .. code-block:: python
    
        dict(http=HTTPCaller(),
           getRootFolder=getRootFolder,
           sync=sync)

    for functional doctests and an empty dict for unit
    doctests. Python test globals can't be set this way.
    
    If you want to register special globals for functional doctest or
    unit doctests only, then you can use the `fglobs` and/or `uglobs`
    keyword respectively. These keywords replace any `globs` value for
    the respective kind of tests.
    
    `setup`
    
    A function that takes a `test` argument and is executed before
    every single doctest. By default it runs::

      zope.app.testing.functional.FunctionalTestSetup().setUp()

    for functional doctests and an empty function for unit
    doctests. Python tests provide their own setups.

    If you want to register special setup-functions for either
    functional or unit doctests, then you can pass keyword parameters
    `fsetup` or `usetup` respectively.
    
    `teardown`
    
    The equivalent to `setup`. Runs by default::

      FunctionalTestSetup().tearDown()

    for functional doctests and::

      zope.testing.cleanup.cleanUp()

    for unit doctests. Python tests have to provide their own teardown
    functions in TestCases.
    
    `optionflags`

    Optionflags influence the behaviour of the testrunner. They are
    logically or'd so that you can add them arithmetically.
    
    `zcml_config`
    
    A filepath of a ZCML file which is registered with functional
    doctests. In the ZCML file you can for example register principals
    (users) usable by functional doctests.

    By default any `ftesting.zcml` file from the root of the given
    package is taken. If this does not exist, an empty ZCML file of
    the z3c.testsetup package is used (``ftesting.zcml``).

    This parameter has no effect, if also a ``layer`` parameter is
    given.
    
    `layer_name`
    
    You can name your layer, to distinguish different setups of
    functional doctests. The layer name can be an arbitrary string.

    This parameter has no effect, if also a ``layer`` parameter is
    given.

    `layer`
    
    You can register a ZCML layer yourself and pass it as the
    ``layer`` parameter. If you only have a filepath to the according
    ZCML file, use the ``zcml_config`` paramter instead.

    This parameter overrides any ``zcml_config`` and ``layer_name``
    parameter.


**Example 1: Boilerplace code put into a tests.py module of a package**

.. code-block:: python

    import grok
    test_suite = grok.testing.register_all_tests('sample')


Python test layer
=================

The declaration `:Test-Layer: python` states the file should be included
as part of the Python test layer. These modules are expected to contain
``unittest.TestCase`` classes.

**Example 1: Simple Python test**

.. code-block:: python

    """
    Do a Python test on the app.

    :Test-Layer: python
    """

    import unittest
    from sample.app import Sample

    class SimpleSampleTest(unittest.TestCase):
        "Test the Sample application"

        def test1(self):
            "Test that something works"
            grokapp = Sample()
            self.assertEqual(list(grokapp.keys()), [])

Unit test layer
===============

The declaration `:Test-Layer: unit` states the file should be included
as part of the doctesting unit test layer. This layer requires no setup
and is for tests which can be quickly run.

**Example 1: Simple doctest**::

    Do a simple doctest test on the app.
    ************************************
    :Test-Layer: unit

    When you create an instance there are no objects in it::

       >>> from sample.app import Sample
       >>> grokapp = Sample()
       >>> list(grokapp.keys())
       []


Functional test layer
=====================

The declaration `:Test-Layer: function` states the file should be included
as part of the functional test layer. The setup for this layer includes a
running Zope 3/Grok server. By default the ``ftesting.zcml`` file in the
test package will be used to do configuration of your functional environment.

**Example 1: Simple functional test**

.. code-block:: python

    """
    Do a functional test on the app.

    :Test-Layer: python
    """
    from sample.app import Sample
    from sample.testing import FunctionalLayer
    from zope.app.testing.functional import FunctionalTestCase
    class SampleFunctionalTest(FunctionalTestCase):
        layer = FunctionalLayer
    class SimpleSampleFunctionalTest(SampleFunctionalTest):
        """ This the app in ZODB. """
        def test_simple(self):
            """ test creating a Sample instance into Zope """
            root = self.getRootFolder()
            root['instance'] = Sample()
            self.assertEqual(root.get('instance').__class__, Sample)
