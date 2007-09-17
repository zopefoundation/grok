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

If a locales dir is set explicitly and contains translations, those
are registered automatically:

  >>> from zope import component
  >>> from zope.i18n.interfaces import ITranslationDomain
  >>> component.getUtility(ITranslationDomain, 'mammoth')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass ...ITranslationDomain>, 'mammoth')

Yet no mammoth domain available.

  >>> import grok
  >>> grok.grok('grok.tests.i18n.i18nexplicitlocales_fixture')
  >>> component.getUtility(ITranslationDomain, 'mammoth')
  <zope.i18n.translationdomain.TranslationDomain object at 0x...>

Here it is.

"""
