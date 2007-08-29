# -*- coding: UTF-8 -*-
"""
There is a url function that can be imported from grok to determine the
absolute URL of objects.

  >>> from grok import url
  
  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> manfred = Mammoth()
  >>> herd['manfred'] = manfred

Now let's use url on some things::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred/index")
  >>> print browser.contents
  http://localhost/herd/manfred/index
  >>> browser.open("http://localhost/herd/manfred/another")
  >>> print browser.contents
  http://localhost/herd/manfred/another
  
We get the views manually so we can do a greater variety of url() calls:

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> index_view = component.getMultiAdapter((manfred, request), name='index')
  >>> url(request, index_view)
  'http://127.0.0.1/herd/manfred/index'
  >>> another_view = component.getMultiAdapter((manfred, request),
  ...                                              name='another')
  >>> url(request, another_view)
  'http://127.0.0.1/herd/manfred/another'

Now let's get a URL for a specific object:

  >>> url(request, manfred)
  'http://127.0.0.1/herd/manfred'

We can get the URL for any object in content-space:

  >>> url(request, herd)
  'http://127.0.0.1/herd'

We can also pass a name along with this, to generate a URL to a
particular view on the object:

  >>> url(request, herd, 'something')
  'http://127.0.0.1/herd/something'

It works properly in the face of non-ascii characters in URLs:

  >>> u = url(request, herd, unicode('árgh', 'UTF-8'))
  >>> u
  'http://127.0.0.1/herd/%C3%A1rgh'
  >>> import urllib
  >>> expected = unicode('http://127.0.0.1/herd/árgh', 'UTF-8')
  >>> urllib.unquote(u).decode('utf-8') == expected
  True
"""
import grok
from grok import url

class Herd(grok.Container, grok.Model):
    pass

class Mammoth(grok.Model):
    pass

grok.context(Mammoth)

class Index(grok.View):
    def render(self):
        return url(self.request, self)
    
class Another(grok.View):
    def render(self):
        return url(self.request, self)
