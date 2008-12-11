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

from grok.rest import GrokMethodNotAllowed

from zope import component
from zope.security.proxy import removeSecurityProxy
from zope.security.checker import selectChecker
from zope.publisher.publish import mapply

from zope.app.publication.http import BaseHTTPPublication, HTTPPublication
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.requestpublicationfactories import \
     BrowserFactory, XMLRPCFactory, HTTPFactory
from zope.app.http.interfaces import IHTTPException

class ZopePublicationSansProxy(object):

    def getApplication(self, request):
        result = super(ZopePublicationSansProxy, self).getApplication(request)
        return removeSecurityProxy(result)

    def traverseName(self, request, ob, name):
        result = super(ZopePublicationSansProxy, self).traverseName(
            request, ob, name)
        if request.getTraversalStack():
            return removeSecurityProxy(result)
        else:
            return result
    
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


class GrokHTTPPublication(ZopePublicationSansProxy, HTTPPublication):
   def callObject(self, request, ob):
       orig = ob
       if not IHTTPException.providedBy(ob):
           ob = component.queryMultiAdapter((ob, request),
                                            name=request.method)
           checker = selectChecker(ob)
           if checker is not None:
               checker.check(ob, '__call__')
           ob = getattr(ob, request.method, None)
           if ob is None:
               raise GrokMethodNotAllowed(orig, request)
       return mapply(ob, request.getPositionalArguments(), request)

class GrokHTTPFactory(HTTPFactory):
    def __call__(self):
        request, publication = super(GrokHTTPFactory, self).__call__()
        return request, GrokHTTPPublication
