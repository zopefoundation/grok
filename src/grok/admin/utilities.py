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
"""Helper functions for grok admin.
"""
import re
from zope.tal.taldefs import attrEscape
from urlparse import urlparse, urlunparse

def getPathLinksForObject(obj, root_url=''):
    """Given an object, this function returns HTML code with links to
    documentation.

    The object must provide a string representation like 'foo.blah
    object at 0x9999999'. Returned is then a string, where 'foo' and
    'blah' are embedded in HTML links to docgrok documentation for foo
    and foo.blah.

    The (optional) ``root_url`` is used to create the links to docgrok
    documentation. It is expected to be the URL, which can generate
    docgrok documentation by appending '/docgrok' to the URL.

    We can use ObjectInfo objects to check this:

      >>> from grok.admin.objectinfo import ObjectInfo
      >>> obj = ObjectInfo(None)
      >>> obj
      <grok.admin.objectinfo.ObjectInfo object at ...>

    Obviously we have a string representation of the required form
    here. So we can get HTML with links to the documentation for
    ``grok``, ``grok.admin`` and so on.
    
      >>> from grok.admin.utilities import getPathLinksForObject
      >>> link = getPathLinksForObject(obj)
      >>> link
      "&lt;<a href='/docgrok/grok/'>grok</a>... object at ..."

    We got a link to the ``grok`` documentation. Also links to
    ``grok.admin``, ``grok.admin.objectinfo`` and
    ``grok.admin.objectinfo.ObjectInfo`` are provided:

      >>> link
      "&lt;...<a href='/docgrok/grok/admin/'>admin</a>... object at ..."

    If we provide a root_url, we will find it in the links:

      >>> link = getPathLinksForObject(obj, 'http://localhost:8080')
      >>> link
      "&lt;<a href='http://localhost:8080/docgrok/grok/'>grok</a>..."

    If no dotted path is included in objects strings representation, a
    simple string without links is returned:
    
      >>> getPathLinksForObject(None)
      "'None'"

    HTML entities should be encoded. We set up a site-manager to get
    an 'illegal' object representation including regular expression
    chars ('+') and no dotted path:

      >>> from zope.app.folder import rootFolder
      >>> root = rootFolder()
      >>> from zope.app.component import site
      >>> sm = site.LocalSiteManager(root)
      >>> root.setSiteManager(sm)
      >>> sm
      <LocalSiteManager ++etc++site>

    This is a strange object identifier. Anyway:

      >>> getPathLinksForObject(sm)
      "'&lt;LocalSiteManager ++etc++site&gt;'"
      
    """
    r_exp = re.compile("'<(.+)( object at .*)>'")
    
    raw = `str(obj)`
    match = r_exp.match(raw)
    if match is None:
        return attrEscape(raw)

    result = "&lt;"
    url = root_url + '/docgrok/'
    for part in match.group(1).split('.'):
        url = url + part + '/'
        result += "<a href='%s'>%s</a>." % (url, part)
    if len(result) and result[-1] == '.':
        result = "%s%s&gt;" % (result[:-1], match.group(2))
        return result
    return raw

def getPathLinksForClass(klass, root_url=''):
    """Given a class or classlike object, this function returns HTML
    code with links to documentation.

    The klass object must provide a string representation like '<class
    foo.Bar>'. Returned is then a string, where 'foo' and
    'Bar' are embedded in HTML links to docgrok documentation for foo
    and foo.Bar.

    The (optional) ``root_url`` is used to create the links to docgrok
    documentation. It is expected to be the URL, which can generate
    docgrok documentation by appending '/docgrok' to the URL.

    We can use class ObjectInfo to check this:

      >>> from grok.admin.objectinfo import ObjectInfo
      >>> ObjectInfo
      <class 'grok.admin.objectinfo.ObjectInfo'>

      >>> from grok.admin.utilities import getPathLinksForClass
      >>> htmlcode = getPathLinksForClass(ObjectInfo)
      >>> htmlcode
      "&lt;class '<a href='/docgrok/grok/'>grok</a>...'&gt;"

    When we provide a root_url the link will include it in the
    href-attribute:

      >>> getPathLinksForClass(ObjectInfo, 'http://localhost')
      "&lt;class '<a href='http://localhost/docgrok/grok/'>grok</a>...'&gt;"

    If the class does not provide an appropriate string
    representation, we will get the representation without any links:

      >>> getPathLinksForClass(None, 'http://localhost')
      "'None'"

    This also works with 'class-like' objects, for instance interfaces
    and their interface-classes:

      >>> from zope.app.folder import rootFolder
      >>> from zope.interface import providedBy
      >>> root = rootFolder()
      >>> iface = list(providedBy(root))[0]
      >>> iface
      <InterfaceClass zope.app.folder.interfaces.IRootFolder>

      >>> getPathLinksForClass(iface)
      "&lt;InterfaceClass '<a href='/docgrok/zope/'>zope</a>...'&gt;"

    HTML entities should be encoded. We set up a site-manager to get
    an 'illegal' object representation including regular expression
    chars ('+') and no dotted path:

      >>> from zope.app.folder import rootFolder
      >>> root = rootFolder()
      >>> from zope.app.component import site
      >>> sm = site.LocalSiteManager(root)
      >>> root.setSiteManager(sm)
      >>> sm
      <LocalSiteManager ++etc++site>

    This is a strange object identifier. Anyway:

      >>> getPathLinksForClass(sm)
      "&lt;LocalSiteManager '<a href='/docgrok/++etc++site/'>...</a>'&gt;"

    """
    r_exp = re.compile(".*<(.*) '?(.+)'?(.*)>.*")
    raw = `str(klass)`
    match = r_exp.match(raw)
    if match is None:
        return attrEscape(raw)

    result = "&lt;%s '" % (match.group(1),)
    url = root_url + '/docgrok/'
    for part in match.group(2).split('.'):
        url = "%s%s/" % (url, part)
        result += "<a href='%s'>%s</a>." % (url, part)
    if len(result) and result[-1] == '.':
        result = "%s'%s&gt;" % (result[:-1], match.group(3))
        return result
    return raw

def getPathLinksForDottedName(name, root_url=''):
    """
    """
    if name is None:
        return ''
    result = ''
    url = root_url + '/docgrok/'
    for part in name.split('.'):
        url = "%s%s/" % (url, part)
        result += "<a href='%s'>%s</a>." % (url, part)
    if len(result) and result.endswith('.'):
        result = result[:-1]
        return result
    return name

def isContainingEvilRegExpChars(strval):
    """Check whether a string contains evil chars.

    'Evil' with respect to regular expressions is a string, that
    contains chars, with a special meaning in regular expressions.

    We indeed must provide a string:

       >>> from grok.admin.utilities import isContainingEvilRegExpChars
       >>> isContainingEvilRegExpChars(None)
       Traceback (most recent call last):
       ...
       TypeError: expected string or buffer

       >>> isContainingEvilRegExpChars('foo')
       False

       >>> isContainingEvilRegExpChars('foo++etc++bar')
       True

       >>> isContainingEvilRegExpChars('foo*bar')
       True

    """
    evil_chars = re.compile('.*(\*|\+|\(|\)|\{|\}).*')
    if evil_chars.match(strval):
        return True
    return False


def getParentURL(url):
    """Compute the parent URL for an object described by URL.

       >>> from grok.admin.utilities import getParentURL
       >>> getParentURL('http://foo:8080/myobj')
       'http://foo:8080/'

       >>> getParentURL('http://foo:8080/myfoo/mybar')
       'http://foo:8080/myfoo/'

    We want an URL always to end with a slash:

       >>> getParentURL('http://foo:8080')
       'http://foo:8080/'

    """
    url_list = list(urlparse(url))
    path = url_list[2]
    if path.endswith('/'):
        path = path[:-1]
    path = path.rsplit('/', 1)[0] + '/'
    url_list[2] = path
    return urlunparse(url_list)
