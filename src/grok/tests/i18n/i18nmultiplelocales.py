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
We can register two or more locale directories per module/package:

Make sure, the domains 'mammoth' and 'cave' are not yet registered:

  >>> from zope import component
  >>> from zope.i18n.interfaces import ITranslationDomain
  >>> component.getUtility(ITranslationDomain, 'mammoth')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass ...ITranslationDomain>, 'mammoth')

  >>> component.getUtility(ITranslationDomain, 'cave')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass ...ITranslationDomain>, 'cave')

Yet no mammoth domain available.

  >>> import grok
  >>> grok.grok('grok.tests.i18n.i18nmultiplelocales_fixture')
  >>> component.getUtility(ITranslationDomain, 'mammoth')
  <zope.i18n.translationdomain.TranslationDomain object at 0x...>

  >>> component.getUtility(ITranslationDomain, 'cave')
  <zope.i18n.translationdomain.TranslationDomain object at 0x...>

Here they are.

"""
