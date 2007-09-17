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

If a non-existing directory is declared as locales dir, an error is
raised:

  >>> import grok
  >>> grok.grok('grok.tests.i18n.i18nillegallocales_fixture')
  Traceback (most recent call last):
   ...
  GrokError: localesdir: directory 'land-of-oz' declared in 'grok.tests.i18n.i18nillegallocales_fixture' as locales directory does not exist.

"""

