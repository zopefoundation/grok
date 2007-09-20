"""
Let's examine Grok's REST support.

Let's create a simple application with REST support::

  >>> from grok.ftests.rest.rest import MyApp
  >>> root = getRootFolder()
  >>> root['app'] = MyApp()

Issue a GET request::

  >>> response = http_call('GET', 'http://localhost/++rest++test/app')
  >>> print response.getBody()
  GET

Issue a POST request::

  >>> response = http_call('POST', 'http://localhost/++rest++test/app')
  >>> print response.getBody()
  POST

Issue a PUT request::

  >>> response = http_call('PUT', 'http://localhost/++rest++test/app')
  >>> print response.getBody()
  PUT

Issue a DELETE request::

  >>> response = http_call('DELETE', 'http://localhost/++rest++test/app')
  >>> print response.getBody()
  DELETE

405: Method not allowed
PUT not supported. GET not supported

Fall-back on base registrations.

Action against sub-object in container.

Test skin story.

Security tests.
"""

import grok

class MyApp(grok.Model, grok.Application):
    pass

class MySkinLayer(grok.IRESTLayer):
    pass

class MySkin(grok.RESTProtocol):
    grok.name('test')
    grok.layer(MySkinLayer)

class MyRest(grok.REST):
    grok.layer(MySkinLayer)
    
    def GET(self):
        return "GET"

    def POST(self):
        return "POST"

    def PUT(self):
        return "PUT"

    def DELETE(self):
        return "DELETE"
    
    
