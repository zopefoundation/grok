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

Test Supporting API
~~~~~~~~~~~~~~~~~~~

.. .. module:: grok.testing

To support testing in Grok-based projects, Grok comes with a couple of
helpers located in the :mod:`grok.testing` module.

.. automodule:: grok.testing
   :members:
   :undoc-members:
   :inherited-members:

   .. autofunction:: grok.testing.grok_component

      Grok a single component.

      This function can be used to grok individual components within a
      doctest, such as adapters. It sets up just enough context for
      some grokking to work, though more complicated grokkers which
      need module context (such as view grokkers) might not work.

      Returns ``True`` or ``False`` depending on whether the grokking
      worked or not.

      A sample doctest could look as follows:

        This defines the object we want to provide an adapter for:

          >>> class Bar(object):
          ...    pass

        This is the interface that we want to adapt to:

          >>> from zope.interface import Interface
          >>> class IFoo(Interface):
          ...    pass

        This is the adapter itself:

          >>> import grokcore.component as grok
          >>> class MyAdapter(grok.Adapter):
          ...    grok.provides(IFoo)
          ...    grok.context(Bar)

        Now we will register the adapter using grok_component():

          >>> from grok.testing import grok, grok_component
          >>> grok('grokcore.component.meta')
          >>> grok_component('MyAdapter', MyAdapter)
          True
  
        The adapter should now be available:

          >>> adapted = IFoo(Bar())
          >>> isinstance(adapted, MyAdapter)
          True


      .. deprecated:: 1.0
         Use :func:`grokcore.component.testing.grok_component` instead.