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

from zope import component
from zope.security.proxy import removeSecurityProxy
from zope.security.checker import selectChecker
from zope.publisher.publish import mapply

from zope.publisher.interfaces.http import IHTTPException
from zope.publisher.interfaces.browser import IBrowserView

from zope.app.publication.http import BaseHTTPPublication, HTTPPublication
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.requestpublicationfactories import \
     BrowserFactory, XMLRPCFactory, HTTPFactory

from grok.interfaces import IGrokSecurityView

class ZopePublicationSansProxy(object):
    """Grok mixin that makes a publisher remove security proxies.

    This mixin overrides three methods from the `IPublication`
    interface (defined in `zope.publisher.interfaces`) to alter their
    security behavior.  The normal Zope machinery wraps a security
    proxy around the application object returned by
    `getApplication()`, and around each of the objects returned as
    `traverseName()` is then called for each URL component.  The
    versions here strip the security proxy off instead, returning the
    bare object (unless the object is a non-Grok view, in which case
    we leave the proxy installed for important security
    reasons).  Non-Grok views however, are handled like Grok views, if
    they provide `grok.interfaces.IGrokSecurityView`.

    Finally, when `callObject()` is asked to render
    the view, we quickly re-install a security proxy on the object, make
    sure that the current user is indeed allowed to invoke `__call__()`,
    then pass the bare object to the rendering machinery.

    The result is that, in place of the elaborate series of security
    checks made during the processing of a normal Zope request, Grok
    makes only a single security check: to see if the view can be
    permissibly rendered or not.

    """
    def getApplication(self, request):
        result = super(ZopePublicationSansProxy, self).getApplication(request)
        return removeSecurityProxy(result)

    def traverseName(self, request, ob, name):
        result = super(ZopePublicationSansProxy, self).traverseName(
            request, ob, name)
        bare_result = removeSecurityProxy(result)
        if IBrowserView.providedBy(bare_result):
            if IGrokSecurityView.providedBy(bare_result):
                return bare_result
            else:
                return result
        else:
            return bare_result

    def callObject(self, request, ob):
        checker = selectChecker(ob)
        if checker is not None:
            checker.check(ob, '__call__')
        return super(ZopePublicationSansProxy, self).callObject(request, ob)


class GrokBrowserPublication(ZopePublicationSansProxy, BrowserPublication):
    """Combines `BrowserPublication` with the Grok sans-proxy mixin.

    In addition to the three methods that are overridden by the
    `ZopePublicationSansProxy`, this class overrides a fourth: the
    `getDefaultTraversal()` method, which strips the security proxy from
    the object being returned by the normal method.

    """
    def getDefaultTraversal(self, request, ob):
        obj, path = super(GrokBrowserPublication, self).getDefaultTraversal(
            request, ob)
        return removeSecurityProxy(obj), path

class GrokBrowserFactory(BrowserFactory):
    """Returns the classes Grok uses for browser requests and publication.

    When an instance of this class is called, it returns a 2-element
    tuple containing:

    - The request class that Grok uses for browser requests.
    - The publication class that Grok uses to publish to a browser.

    """
    def __call__(self):
        request, publication = super(GrokBrowserFactory, self).__call__()
        return request, GrokBrowserPublication


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
