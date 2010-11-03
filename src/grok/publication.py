##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Grok publication factories and classes.

These factories, and the publication classes they return, make Grok
security different from the way that security normal operates during
Zope publication.  Instead of security proxies being wrapped around
every object generated during traversal, and then wrapped around the
final object before it is viewed, only a single security check is done
when Grok is in charge: a check to see whether the view selected at the
end of the traversal process is, in fact, permitted to display the
object.

"""
from grok.rest import GrokMethodNotAllowed
from grokcore.view.publication import ZopePublicationSansProxy

from zope import component
from zope.security.checker import selectChecker
from zope.publisher.publish import mapply
from zope.publisher.interfaces.http import IHTTPException

from zope.app.publication.http import BaseHTTPPublication, HTTPPublication
from zope.app.publication.requestpublicationfactories import (
    XMLRPCFactory, HTTPFactory)


class GrokXMLRPCPublication(ZopePublicationSansProxy, BaseHTTPPublication):
    """Combines `BaseHTTPPublication` with the Grok sans-proxy mixin."""


class GrokXMLRPCFactory(XMLRPCFactory):
    """Returns the classes Grok uses for browser requests and publication.

    When an instance of this class is called, it returns a 2-element
    tuple containing:

    - The request class that Grok uses for XML-RPC requests.
    - The publication class that Grok uses to publish to a XML-RPC.

    """
    def __call__(self):
        request, publication = super(GrokXMLRPCFactory, self).__call__()
        return request, GrokXMLRPCPublication


class GrokHTTPPublication(ZopePublicationSansProxy, HTTPPublication):
    """Combines `HTTPPublication` with the Grok sans-proxy mixin.

    Because `HTTPPublication` provides its own, special `callObject()`
    implementation, this subclass does the same, providing what is
    basically the same call (you can verify, in fact, that most of its
    lines were copied directly from the superclass's version) but with a
    few extra lines added so that - as with the simpler `callObject()`
    method in `ZopePublicationSansProxy` - it quickly places a security
    proxy around the object, makes sure that this HTTP method is
    permitted, and finally passes the bare object to the view that will
    render it.

    """
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
    """Returns the classes Grok uses for HTTP requests and publication.

    When an instance of this class is called, it returns a 2-element
    tuple containing:

    - The request class that Grok uses for HTTP requests.
    - The publication class that Grok uses to publish to HTTP.

    """
    def __call__(self):
        request, publication = super(GrokHTTPFactory, self).__call__()
        return request, GrokHTTPPublication
