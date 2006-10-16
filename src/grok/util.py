##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Grok utility functions.
"""

import re
import types


def not_unicode_or_ascii(value):
    if isinstance(value, unicode):
        return False
    if not isinstance(value, str):
        return True
    return is_not_ascii(value)

is_not_ascii = re.compile(eval(r'u"[\u0080-\uffff]"')).search

def isclass(obj):
    """We cannot use ``inspect.isclass`` because it will return True for interfaces"""
    return type(obj) in (types.ClassType, type)

def check_subclass(obj, class_):
    if not isclass(obj):
        return False
    return issubclass(obj, class_)

