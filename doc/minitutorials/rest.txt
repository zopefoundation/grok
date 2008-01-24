REST support in Grok
====================

:Author: Martijn Faassen

REST_ is a way to build web services, i.e. a web application where the
user is another computer, not a human being. REST takes the approach
to make the web service look very similar to a normal web application,
using well-known semantics of HTTP.

.. _REST: http://en.wikipedia.org/wiki/Representational_State_Transfer

Grok has support that helps you implement REST-based protocols. That
is, Grok doesn't actually implement any RESTful protocols itself, but
it allows you to easily add them in your own application.

To implement a REST protocol, you do something very similar to
implementing a skin. This way, REST requests are separated from other
requests on objects. This means you can have a normal web UI with
views on a set of objects in parallel to the implementation of one or
more REST protocols.

Let's see how you define a REST protocol. Similar to the way skins
work, first you need to define a layer. In the case of REST, your
layer must derive from grok.IRESTLayer::

  class AtomPubLayer(grok.IRESTLayer):
     pass

REST handlers are very much like views like JSON or XMLRPC views. In
the case of REST, you implement the HTTP methods on the view::

  class MyREST(grok.REST):
      grok.context(MyContainer)

    def GET(self):
        return "GET request, retrieve container listing"

    def POST(self):
        return "POST request, add something to container"

    def PUT(self):
        return "PUT request, replace complete contents"

    def DELETE(self):
        return "DELETE request, delete this object entirely"

When handling a REST request, you often want to get to the raw body of
the request. You can access a special ``body`` attributre that contains
the body as a string::

  class MyREST2(grok.REST):
      def POST(self):
          return "This is the body: " + self.body

This body should be parsed accordingly by your REST protocol
implementation - it could for instance be some form of XML or JSON.

To actually issue REST requests over a URL, you need to define a REST
protocol that uses this layer::

  class AtomPubProtocol(grok.RESTProtocol):
     grok.layer(AtomPubLayer)
     grok.name('atompub') # a nicer name

Again this is very similar to the way skins work - in order to use a
layer you need to define a ``grok.Skin`` first.

Now you can access the object with the REST protocol, through requests
like this (issuing GET, POST, PUT or DELETE)::

  http://localhost:8080/++rest++atompub/mycontainer

As you can see, you need to use the ++rest++<protocolname> pattern
somewhere in the URL in order to access the REST view for your
objects. If you don't like the ++rest++ bit you can also provide
(``directlyProvides``) the layer manually to the request during traversal,
or if you're using Apache, use a few rewrite rules. (just like with
skins).

Using protocols like this means you could have a single object
implement several different REST protocols. Since layers are used, you
could also compose a single REST protocols out of multiple protocols
should you so desire.

If you don't explicitly set a layer using ``grok.layer`` for a REST
subclass, it'll use the grok.IRESTLayer by default. This layer is the
base of all REST layers.

Similar again to XMLRPC or JSON views, security works with all this:
you can use @grok.require() on the REST methods to shield them from
public use.
