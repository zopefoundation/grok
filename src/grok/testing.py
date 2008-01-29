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
"""Grok test helpers
"""
from zope.configuration.config import ConfigurationMachine
from martian import scan
from grok import zcml

import unittest
from os import listdir
import os.path
import re
from zope.testing import doctest, cleanup
from zope.app.testing.functional import (
    HTTPCaller, getRootFolder, FunctionalTestSetup,
    sync, ZCMLLayer, FunctionalDocFileSuite)

class BasicTestSetup(object):
    """A basic test setup for a package.

    A basic test setup is a aggregation of methods and attributes to
    search for appropriate doctest files in a package. Its purpose is
    to collect all basic functionality, that is needed by derived
    classes, that do real test registration.
    """

    extensions = ['.rst', '.txt']

    regexp_list = []

    additional_options = {}

    def __init__(self, package, filter_func=None, extensions=None, **kw):
        self.package = package
        self.filter_func = filter_func or self.isTestFile
        self.extensions = extensions or self.extensions
        self.additional_options = kw
        return

    def setUp(self, test):
        pass

    def tearDown(self, test):
        pass

    def fileContains(self, filename, regexp_list):
        """Does a file contain lines matching every of the regular
        expressions?
        """
        found_list = []
        try:
            for line in open(filename):
                for regexp in regexp_list:
                    if re.compile(regexp).match(line) and (
                        regexp not in found_list):
                        found_list.append(regexp)
                if len(regexp_list) == len(found_list):
                    break
        except IOError:
            # be gentle
            pass
        return len(regexp_list) == len(found_list)

    def isTestFile(self, filepath):
        """Return ``True`` if a file matches our expectations for a
        doctest file.
        """
        if os.path.splitext(filepath)[1].lower() not in self.extensions:
            return False
        if not self.fileContains(filepath, self.regexp_list):
            return False
        return True

    def isTestDirectory(self, dirpath):
        """Check whether a given directory should be searched for tests.
        """
        if os.path.basename(dirpath).startswith('.'):
            # We don't search hidden directories like '.svn'
            return False
        return True

    def getDocTestFiles(self, dirpath=None, **kw):
        """Find all doctest files filtered by filter_func.
        """
        if dirpath is None:
            dirpath = os.path.dirname(self.package.__file__)
        dirlist = []
        for filename in listdir(dirpath):
            abs_path = os.path.join(dirpath, filename)
            if not os.path.isdir(abs_path):
                if self.filter_func(abs_path):
                    dirlist.append(abs_path)
                continue
            # Search subdirectories...
            if not self.isTestDirectory(abs_path):
                continue
            subdir_files = self.getDocTestFiles(dirpath=abs_path, **kw)
            dirlist.extend(subdir_files)
        return dirlist


class UnitTestSetup(BasicTestSetup):
    """A unit test setup for packages.

    A collection of methods to search for appropriate doctest files in
    a given package. ``UnitTestSetup`` is also able to 'register' the
    tests found and to deliver them as a ready-to-use
    ``unittest.TestSuite`` instance.

    While the functionality to search for testfiles is mostly
    inherited from the base class, the focus here is to setup the
    tests correctly.

    See file `unittestsetup.py` in the tests/testsetup directory to
    learn more about ``UnitTestSetup``.
    """

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(unit)\s*',
        ]


    def tearDown(self, test):
        cleanup.cleanUp()

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            if os.path.isabs(name):
                # We get absolute pathnames, but we need relative ones...
                common_prefix = os.path.commonprefix([self.package.__file__,
                                                      name])
                name = name[len(common_prefix):]
            suite.addTest(
                doctest.DocFileSuite(
                name,
                package=self.package,
                setUp=self.setUp,
                tearDown=self.tearDown,
                optionflags=self.optionflags,
                **self.additional_options
                ))
        return suite


class FunctionalTestSetup(BasicTestSetup):
    """A functional test setup for packages.

    A collection of methods to search for appropriate doctest files in
    a given package. ``FunctionalTestSetup`` is also able to
    'register' the tests found and to deliver them as a ready-to-use
    ``unittest.TestSuite`` instance.

    While the functionality to search for testfiles is mostly
    inherited from the base class, the focus here is to setup the
    tests correctly.
    """
    ftesting_zcml = os.path.join(os.path.dirname(__file__),
                                 'ftesting.zcml')
    layer = ZCMLLayer(ftesting_zcml, __name__,
                      'FunctionalLayer')

    globs=dict(http=HTTPCaller(),
               getRootFolder=getRootFolder,
               sync=sync
               )

    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    regexp_list = [
        '^\s*:(T|t)est-(L|l)ayer:\s*(functional)\s*',
        ]

    def setUp(self, test):
        FunctionalTestSetup().setUp()

    def tearDown(self, test):
        FunctionalTestSetup().tearDown()

    def suiteFromFile(self, name):
        suite = unittest.TestSuite()
        if os.path.isabs(name):
            # We get absolute pathnames, but we need relative ones...
            common_prefix = os.path.commonprefix([self.package.__file__, name])
            name = name[len(common_prefix):]
        test = FunctionalDocFileSuite(
            name, package=self.package,
            setUp=self.setUp, tearDown=self.tearDown,
            globs=self.globs,
            optionflags=self.optionflags,
            **self.additional_options
            )
        test.layer = self.layer
        suite.addTest(test)
        return suite

    def getTestSuite(self):
        docfiles = self.getDocTestFiles(package=self.package)
        suite = unittest.TestSuite()
        for name in docfiles:
            suite.addTest(self.suiteFromFile(name))
        return suite


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grok.meta', config)
    zcml.do_grok('grok.templatereg', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()

def grok_component(name, component,
                   context=None, module_info=None, templates=None):
    if module_info is None:
        obj_module = getattr(component, '__grok_module__', None)
        if obj_module is None:
            obj_module = getattr(component, '__module__', None)
        module_info = scan.module_info_from_dotted_name(obj_module)

    module = module_info.getModule()
    if context is not None:
        module.__grok_context__ = context
    if templates is not None:
        module.__grok_templates__ = templates
    config = ConfigurationMachine()
    result = zcml.the_multi_grokker.grok(name, component,
                                         module_info=module_info,
                                         config=config)
    config.execute_actions()    
    return result
