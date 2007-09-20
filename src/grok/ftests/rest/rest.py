"""
Let's examine Grok's REST support.

Let's create a simple application with REST support::

  >>> from grok.ftests.rest.rest import MyApp
  >>> root = getRootFolder()
  >>> root['app'] = MyApp()
  >>> root['app']['alpha'] = MyContent()
  
Issue a GET request::

  >>> response = http_call('GET', 'http://localhost/++rest++a/app')
  >>> print response.getBody()
  GET

Issue a POST request::

  >>> response = http_call('POST', 'http://localhost/++rest++a/app')
  >>> print response.getBody()
  POST

Issue a PUT request::

  >>> response = http_call('PUT', 'http://localhost/++rest++a/app')
  >>> print response.getBody()
  PUT

Issue a DELETE request::

  >>> response = http_call('DELETE', 'http://localhost/++rest++a/app')
  >>> print response.getBody()
  DELETE

Let's examine a rest protocol b which has no POST or DELETE request defined::

The GET request works as expected::

  >>> response = http_call('GET', 'http://localhost/++rest++b/app')
  >>> print response.getBody()
  GET

So does the PUT request::

  >>> response = http_call('PUT', 'http://localhost/++rest++b/app')
  >>> print response.getBody()
  PUT

POST is not defined, however, and we should get a 405 (Method not
allowed) error::

  >>> response = http_call('POST', 'http://localhost/++rest++b/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.browser.BrowserRequest instance URL=http://localhost/++rest++b/app/@@POST>

DELETE is also not defined, so we also expect a 405 error::

  >>> response = http_call('DELETE', 'http://localhost/++rest++b/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.http.HTTPRequest instance URL=http://localhost/++rest++b/app>

Let's examine protocol c where no method is allowed::

  >>> response = http_call('GET', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('POST', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('PUT', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('DELETE', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...

Let's examine the default protocol d, where nothing should work as well::

  >>> response = http_call('GET', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('POST', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('PUT', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('DELETE', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  
We have added support for GET for the ``alpha`` subobject only, in
the default rest layer::

  >>> response = http_call('GET', 'http://localhost/++rest++d/app/alpha')
  >>> response.getBody()
  'GET2'

But not for POST::

  >>> response = http_call('POST', 'http://localhost/++rest++d/app/alpha')
  Traceback (most recent call last):
    ...
  MethodNotAllowed: <grok.ftests.rest.rest.MyContent object at ...

Todo:

* MethodNotAllowed error URLs for GET and POST have @@GET and @@POST
  attached. Not pretty.

* Security tests.

* According to HTTP spec: 405 Method Not Allowed:
  The response MUST include an Allow header containing a list of valid
  methods for the requested resource.
"""

import grok

class MyApp(grok.Container, grok.Application):
    pass

class MyContent(grok.Model):
    pass

class LayerA(grok.IRESTLayer):
    pass

class LayerB(grok.IRESTLayer):
    pass

class LayerC(grok.IRESTLayer):
    pass

class A(grok.RESTProtocol):
    grok.layer(LayerA)

class B(grok.RESTProtocol):
    grok.layer(LayerB)

class C(grok.RESTProtocol):
    grok.layer(LayerC)

class D(grok.RESTProtocol):
    grok.layer(grok.IRESTLayer)

class ARest(grok.REST):
    grok.layer(LayerA)
    grok.context(MyApp)
    
    def GET(self):
        return "GET"

    def POST(self):
        return "POST"

    def PUT(self):
        return "PUT"

    def DELETE(self):
        return "DELETE"

class BRest(grok.REST):
    grok.layer(LayerB)
    grok.context(MyApp)
    
    def GET(self):
        return "GET"

    def PUT(self):
        return "PUT"

class CRest(grok.REST):
    grok.layer(LayerC)
    grok.context(MyApp)

class DRest(grok.REST):
    grok.context(MyContent)
    
    def GET(self):
        return "GET2"
