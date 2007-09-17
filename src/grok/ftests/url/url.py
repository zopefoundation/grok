# -*- coding: UTF-8 -*-
"""
Views have a method that can be used to construct URLs:

  >>> herd = Herd()
  >>> getRootFolder()['herd'] = herd
  >>> manfred = Mammoth()
  >>> herd['manfred'] = manfred

The views in this test implement self.url():

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred/index")
  >>> print browser.contents
  http://localhost/herd/manfred/index
  >>> browser.open("http://localhost/herd/manfred/another")
  >>> print browser.contents
  http://localhost/herd/manfred/another
  >>> browser.open("http://localhost/herd/manfred/yetanother")
  >>> print browser.contents
  http://localhost/herd/manfred/yetanother
  
We get the views manually so we can do a greater variety of url() calls:

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> index_view = component.getMultiAdapter((manfred, request), name='index')
  >>> index_view.url()
  'http://127.0.0.1/herd/manfred/index'
  >>> another_view = component.getMultiAdapter((manfred, request),
  ...                                              name='another')
  >>> another_view.url()
  'http://127.0.0.1/herd/manfred/another'
  >>> yet_another_view = component.getMultiAdapter((manfred, request),
  ...                                              name='yetanother')
  >>> yet_another_view.url()
  'http://127.0.0.1/herd/manfred/yetanother'

Now let's get a URL for a specific object:

  >>> index_view.url(manfred)
  'http://127.0.0.1/herd/manfred'

This works with any other view too (as they share the same request):

  >>> another_view.url(manfred)
  'http://127.0.0.1/herd/manfred'

This shows that the default argument is the view itself:

  >>> another_view.url(another_view)
  'http://127.0.0.1/herd/manfred/another'

We can get the URL for any object in content-space:

  >>> another_view.url(herd)
  'http://127.0.0.1/herd'

We can also pass a name along with this, to generate a URL to a
particular view on the object:

  >>> another_view.url(herd, 'something')
  'http://127.0.0.1/herd/something'

It works properly in the face of non-ascii characters in URLs:

  >>> url = another_view.url(herd, unicode('árgh', 'UTF-8'))
  >>> url
  'http://127.0.0.1/herd/%C3%A1rgh'
  >>> import urllib
  >>> expected = unicode('http://127.0.0.1/herd/árgh', 'UTF-8')
  >>> urllib.unquote(url).decode('utf-8') == expected
  True

It's also possible to just pass in a name. In this case, a URL to that
view on the context object will be constructed:

  >>> another_view.url('yet_another_view')
  'http://127.0.0.1/herd/manfred/yet_another_view'

Some combinations of arguments just don't make sense:

  >>> another_view.url('foo', 'bar')
  Traceback (most recent call last):
    ...
  TypeError: url() takes either obj argument, obj, string arguments, or
  string argument
  >>> another_view.url('foo', herd)
  Traceback (most recent call last):
    ...
  TypeError: url() takes either obj argument, obj, string arguments, or
  string argument
  >>> another_view.url(herd, 'bar', 'baz')
  Traceback (most recent call last):
    ...
  TypeError: url() takes at most 3 arguments (4 given)
  
"""
import grok

class Herd(grok.Container, grok.Model):
    pass

class Mammoth(grok.Model):
    pass

grok.context(Mammoth)

class Index(grok.View):
    def render(self):
        return self.url()
    
class Another(grok.View):
    def render(self):
        return self.url()

class YetAnother(grok.View):
    pass

yetanother = grok.PageTemplate('<p tal:replace="view/url" />')
