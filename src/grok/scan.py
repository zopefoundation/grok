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
"""Scanning packages and modules
"""

import os
import setuptools
from glob import glob
from zope.dottedname.resolve import resolve

#TODO: not ZIP-safe
def modules(dotted_name, module_path):
    yield dotted_name

    if not (module_path.endswith('__init__.py')
            or module_path.endswith('__init__.pyc')):
        return

    package_directory = os.path.dirname(module_path)
    seen = []
    for entry in sorted(os.listdir(package_directory)):
        entry_path = os.path.join(package_directory, entry)

        if entry in ['__init__.py', '__init__.pyc']:
            continue
        elif os.path.isfile(entry_path) and (entry.endswith('.py')
                                        or entry.endswith('.pyc')):
            module_name = os.path.splitext(entry)[0]
            if module_name in seen:
                continue
            seen.append(module_name)
            yield '%s.%s' % (dotted_name, module_name)
        else:
            if os.path.isdir(entry_path):
                init_py = os.path.join(entry_path, '__init__.py')
                init_pyc = os.path.join(entry_path, '__init__.pyc')

                if os.path.exists(init_py):
                    init_path = init_py
                elif os.path.exists(init_pyc):
                    init_path = init_pyc
                else:
                    continue

                for name in modules('%s.%s' % (dotted_name, entry), init_path):
                    yield name
