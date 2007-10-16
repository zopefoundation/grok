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
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.browser.BrowserRequest instance URL=http://localhost/++rest++b/app>

DELETE is also not defined, so we also expect a 405 error::

  >>> response = http_call('DELETE', 'http://localhost/++rest++b/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...>,
  <zope.publisher.http.HTTPRequest instance URL=http://localhost/++rest++b/app>

Let's examine protocol c where no method is allowed::

  >>> response = http_call('GET', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('POST', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('PUT', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('DELETE', 'http://localhost/++rest++c/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...

Let's examine the default protocol d, where nothing should work as well::

  >>> response = http_call('GET', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('POST', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('PUT', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  >>> response = http_call('DELETE', 'http://localhost/++rest++d/app')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyApp object at ...
  
We have added support for GET for the ``alpha`` subobject only, in
the default rest layer::

  >>> response = http_call('GET', 'http://localhost/++rest++d/app/alpha')
  >>> response.getBody()
  'GET2'

But not for POST::

  >>> response = http_call('POST', 'http://localhost/++rest++d/app/alpha')
  Traceback (most recent call last):
    ...
  GrokMethodNotAllowed: <grok.ftests.rest.rest.MyContent object at ...

According to the HTTP spec, in case of a 405 Method Not Allowed error,
the response MUST include an Allow header containing a list of valid
methods for the requested resource::

  >>> print http('POST /++rest++b/app HTTP/1.1')
  HTTP/1. 405 Method Not Allowed
  Allow: GET, PUT
  Content-Length: 18
  Content-Type: text/plain
  <BLANKLINE>
  Method Not Allowed

  >>> print http('DELETE /++rest++b/app HTTP/1.1')
  HTTP/1. 405 Method Not Allowed
  Allow: GET, PUT
  Content-Length: 18
  <BLANKLINE>
  Method Not Allowed
  
  >>> print http('POST /++rest++c/app HTTP/1.1')
  HTTP/1. 405 Method Not Allowed
  Allow: 
  Content-Length: 18
  Content-Type: text/plain
  <BLANKLINE>
  Method Not Allowed

We can also try this with a completely made-up request method, like FROG::

  >>> print http('FROG /++rest++b/app HTTP/1.1')
  HTTP/1. 405 Method Not Allowed
  Allow: GET, PUT
  Content-Length: 18
  <BLANKLINE>
  Method Not Allowed

Let's now see whether security works properly with REST. GET should
be public::

  >>> print http('GET /++rest++e/app/alpha HTTP/1.1')
  HTTP/1. 200 Ok
  Content-Length: 4
  Content-Type: text/plain
  <BLANKLINE>
  GET3

POST, PUT and DELETE however are not public::

  >>> print http('POST /++rest++e/app/alpha HTTP/1.1')
  HTTP/1. 401 Unauthorized
  Content-Length: 0
  Content-Type: text/plain
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

  >>> print http('PUT /++rest++e/app/alpha HTTP/1.1')
  HTTP/1. 401 Unauthorized
  Content-Length: 0
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

  >>> print http('DELETE /++rest++e/app/alpha HTTP/1.1')
  HTTP/1. 401 Unauthorized
  Content-Length: 0
  WWW-Authenticate: basic realm="Zope"
  <BLANKLINE>

Normally when we POST or PUT a request, we expect some content. This
content is sent along as the request body. In the normal case for POST
we tend to retrieve this information from a web form (request.form),
but with REST often the POST body contains a description of an
entirely new resource, similar to what is contained in a PUT body. We
therefore need to have some easy way to get to this information. The 'body'
attribute on the REST view contains the uploaded data::

  >>> print http_call('POST', 'http://localhost/++rest++f/app/alpha',
  ...                 'this is the POST body')
  HTTP/1.1 200 Ok
  Content-Length: 21
  Content-Type: text/plain
  <BLANKLINE>
  this is the POST body

This works with PUT as well::

  >>> print http_call('PUT', 'http://localhost/++rest++f/app/alpha',
  ...                 'this is the PUT body')
  HTTP/1.1 200 Ok
  Content-Length: 20
  <BLANKLINE>
  this is the PUT body

Todo:

* Support for OPTIONS, HEAD, other methods?

* Content-Type header is there for GET/POST, but not for PUT/DELETE...
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

class LayerSecurity(grok.IRESTLayer):
    pass

class LayerContent(grok.IRESTLayer):
    pass

class A(grok.RESTProtocol):
    grok.layer(LayerA)

class B(grok.RESTProtocol):
    grok.layer(LayerB)

class C(grok.RESTProtocol):
    grok.layer(LayerC)

class D(grok.RESTProtocol):
    grok.layer(grok.IRESTLayer)

class E(grok.RESTProtocol):
    grok.layer(LayerSecurity)

class F(grok.RESTProtocol):
    grok.layer(LayerContent)
    
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

class SecurityRest(grok.REST):
    grok.context(MyContent)
    grok.layer(LayerSecurity)
    
    @grok.require('zope.Public')
    def GET(self):
        return "GET3"

    @grok.require('zope.ManageContent')
    def POST(self):
        return "POST3"

    @grok.require('zope.ManageContent')
    def PUT(self):
        return "PUT3"

    @grok.require('zope.ManageContent')
    def DELETE(self):
        return "DELETE3"
    
class BodyTest(grok.REST):
    grok.context(MyContent)
    grok.layer(LayerContent)

    def POST(self):
        return self.body

    def PUT(self):
        return self.body
    
