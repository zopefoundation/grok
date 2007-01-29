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
"""Grok publication objects
"""
import transaction
import ZODB.Connection

from zope.security.proxy import removeSecurityProxy
from zope.security.checker import selectChecker
from zope.publisher.interfaces import Redirect

from zope.app.publication.http import BaseHTTPPublication
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.requestpublicationfactories import \
     BrowserFactory, XMLRPCFactory

from grok._grok import check_reload, reload_grokked_modules

class ZopePublicationSansProxy(object):

    def openedConnection(self, conn):
        if check_reload():
            reload_grokked_modules()

            # Reset ZODB's pickle caches so that persistent objects
            # use the new classes.
            # XXX doesn't work?!?
            ZODB.Connection.resetCaches()
            transaction.commit()
            conn._resetCache()
            transaction.begin()

    def getApplication(self, request):
        result = super(ZopePublicationSansProxy, self).getApplication(request)
        return removeSecurityProxy(result)

    def traverseName(self, request, ob, name):
        result = super(ZopePublicationSansProxy, self).traverseName(
            request, ob, name)
        return removeSecurityProxy(result)

    def callObject(self, request, ob):
        checker = selectChecker(ob)
        if checker is not None:
            checker.check(ob, '__call__')
        return super(ZopePublicationSansProxy, self).callObject(request, ob)


class GrokBrowserPublication(ZopePublicationSansProxy, BrowserPublication):

    def getDefaultTraversal(self, request, ob):
        obj, path = super(GrokBrowserPublication, self).getDefaultTraversal(
            request, ob)
        return removeSecurityProxy(obj), path


class GrokBrowserFactory(BrowserFactory):

    def __call__(self):
        request, publication = super(GrokBrowserFactory, self).__call__()
        return request, GrokBrowserPublication


class GrokXMLRPCPublication(ZopePublicationSansProxy, BaseHTTPPublication):
    pass


class GrokXMLRPCFactory(XMLRPCFactory):

    def __call__(self):
        request, publication = super(GrokXMLRPCFactory, self).__call__()
        return request, GrokXMLRPCPublication
