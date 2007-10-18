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
"""I18n support for grok.

You can find a (more or less) complete i18n-example in ftests.i18n.
"""

import os
import grok

from zope.component import provideUtility
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.testmessagecatalog import TestMessageCatalog
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.interfaces import ITranslationDomain


def registerTranslationsDirectory(directory):
    """A replacement for the ZCML registerTranslations directive.

    Basically, this is the same code as in zope.i18n.zcml, but it
    calls ``provideUtility()`` directly.
    """
    path = os.path.normpath(directory)
    domains = {}

    # Gettext has the domain-specific catalogs inside the language directory,
    # which is exactly the opposite as we need it. So create a dictionary that
    # reverses the nesting.
    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')
        if os.path.isdir(lc_messages_path):
            for domain_file in os.listdir(lc_messages_path):
                if domain_file.endswith('.mo'):
                    domain_path = os.path.join(lc_messages_path, domain_file)
                    domain = domain_file[:-3]
                    if not domain in domains:
                        domains[domain] = {}
                    domains[domain][language] = domain_path

    # Now create TranslationDomain objects and add them as utilities
    for name, langs in domains.items():
        domain = TranslationDomain(name)

        for lang, file in langs.items():
            domain.addCatalog(GettextMessageCatalog(lang, name, file))

        # make sure we have a TEST catalog for each domain:
        domain.addCatalog(TestMessageCatalog(name))
        # TODO: We might do some permissions checking before.
        provideUtility(domain, ITranslationDomain, name)
    return

