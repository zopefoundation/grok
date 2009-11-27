"""
Let's examine Grok's REST support in the context of custom traversal to
verify that works. We set the REST protocol in the code instead of specifying
it in the URL, just in time (when we traverse to the content object that
supports REST).

Let's create a simple application with REST support::

  >>> from grok.ftests.rest.rest_traverse import MyApp
  >>> root = getRootFolder()
  >>> root['app'] = MyApp()

Let's first look at the index view of the application object::

  >>> response = http_call('GET', 'http://localhost/app')
  >>> print response.getBody()
  The index view

Now let's look at the content subobject, which should use REST by default
because we make sure we set the skin::

  >>> response = http_call('GET', 'http://localhost/app/content')
  >>> print response.getBody()
  GET content

The other methods should also work::

  >>> response = http_call('POST', 'http://localhost/app/content')
  >>> print response.getBody()
  POST content

  >>> response = http_call('PUT', 'http://localhost/app/content')
  >>> print response.getBody()
  PUT content

  >>> response = http_call('DELETE', 'http://localhost/app/content')
  >>> print response.getBody()
  DELETE content

Besides the Traverser, we also want to make sure our ``traverse`` method
on content objects works::

  >>> response = http_call('GET', 'http://localhost/app/content/sub')
  >>> print response.getBody()
  GET content
  >>> response = http_call('PUT', 'http://localhost/app/content/sub')
  >>> print response.getBody()
  PUT content

"""

import grok
from zope.interface import Interface
from grok.util import applySkin

class IFoo(Interface):
    pass

class MyApp(grok.Model, grok.Application):
    pass

class Traverser(grok.Traverser):
    grok.context(MyApp)

    def traverse(self, name):
        if name == 'content':
            applySkin(self.request, LayerZ, grok.IRESTSkinType)
            return MyContent()

class Index(grok.View):
    grok.context(MyApp)
    def render(self):
        return "The index view"

class MyContent(grok.Model):
    def traverse(self, name):
        if name == 'sub':
            return MyContent()

class LayerZ(grok.IRESTLayer):
    grok.restskin('layerz')

class ZContentRest(grok.REST):
    grok.layer(LayerZ)
    grok.context(MyContent)

    def GET(self):
        return "GET content"

    def POST(self):
        return "POST content"

    def PUT(self):
        return "PUT content"

    def DELETE(self):
        return "DELETE content"
