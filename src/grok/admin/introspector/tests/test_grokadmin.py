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
Test setup for grok.admin.introspector.
"""
from grok.testing import register_all_tests
from grok.ftests.test_grok_functional import GrokFunctionalLayer
# This we say: include all testfiles in or below the
# grok.admin.introspector package in the tests.
#
test_suite = register_all_tests('grok.admin.introspector',
                                layer=GrokFunctionalLayer)
