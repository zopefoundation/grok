Grok Developer's Notes
======================

This document is a developer's overview of Grok. It is not intended to
be a beginner's tutorial. It's also not a reference. It gives a
succinct an overview of *what's there* in Grok, with a brief idea on
how to use it, so you can try it out and learn more about it. This
includes rules, common APIs and patterns.

Models
------

A Grok-based application is composed out of one or more *models*. We
also call these *content objects*, or just *objects*. The objects are
just Python objects, instantiated from a class. Models can be stored
in the object database (ZODB), created by an object relational mapper,
or created on the fly by your code.

Grok comes with two kinds of models: ``grok.Model`` and
``grok.Container``. ``grok.Model`` is the most basic one and doesn't
really do much for you. You can subclass from ``grok.Model``, like
this::

  class Document(grok.Model):
      pass

The main thing subclassing from ``grok.Model`` does is make it
possible (but not required) to store instances in the ZODB.

You can also subclass from ``grok.Container``, like this::

  class Folder(grok.Container):
      pass

A container is like a model, but also acts much like a Python
dictionary. The main difference with Python dictionaries is that its
methods, like ``keys`` and ``items``, are iterator-like. They also do
more, like send events, but we can forget about that for now.

In order to be able to install an application, you need to mix in
``grok.Application`` into a class::

  class Application(grok.Application, grok.Container):
      pass

Instances of this class can now be installable in the Grok web UI.

Let's make a structure with some folders and documents::

  app = Application()
  app['a'] = a = Container()
  a['b'] = Document()
  a['c'] = Container()
  a['c']['d'] = Document()

Grok publishes these objects to the web: this is called object
publishing. What this means in essence is that objects can be
addressed with URLs. When you access a URL of a Grok application with
your web browser, Grok uses this URL to find an object.

An example: if ``app`` were installed under
``http://localhost:8080/app``, the following URLs will exist in your
application::

  http://localhost:8080/app
  http://localhost:8080/app/a
  http://localhost:8080/app/a/b
  http://localhost:8080/app/a/c
  http://localhost:8080/app/a/c/d

``__parent__`` and ``__name__``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Models in Grok are automatically supplied with a ``__parent__`` and a
``__name__`` attribute.

* ``__parent__`` points to object this object is in. If the object is in
  a container, this is the container.

* ``__name__`` is the name this object has in a URL (and in its
  container, if it is in a container).

These attributes are used for navigation through content space, and
Grok also uses them to construct URLs automatically (see below). The
``__parent__`` and ``__name__`` attributes are automatically added to
an object when it is placed in a container, or when it is being
traversed through using ``traverse``.

Custom traversing
~~~~~~~~~~~~~~~~~

Grok resolves URLs to objects by *traversing* through the containers
and models in question. What if you want to customize the way this
traversal works? Perhaps you want to traverse through objects you
create yourself, or objects created by an object relational
mapper. Grok offers a handy way to do so: the ``traverse`` method on
models.

A math example: imagine you want to create an application that
represents integer numbers, and you want to traverse to each
individual number, like this::

  http://localhost:8080/integers/0
  http://localhost:8080/integers/1
  http://localhost:8080/integers/2
  http://localhost:8080/integers/3
  ...

and so on. How would we implement this? We cannot create a container
and fill it with all integers possible, as there are an infinite
number of them. Okay, so we are in a math example, so let's be exact:
this is true if we ignore memory limitations and URL length
limitations. Storing all possible integers in a container is just not
*practical*.

We use the ``traverse`` method::

  class ParticularInteger(grok.Model):
      def __init__(self, number):
          self.number = number

  class Integers(grok.Application, grok.Model):
      def traverse(self, name):
          try:
               value = int(name)
          except ValueError:
               return None # not an integer
          return ParticularInteger(value)

Now all URLs for numbers are available. What's more, other URLs like
this are not::

  http://localhost:8080/integers/foo

The ``traverse`` method works by trying to convert the path element
that comes in as ``name`` to an integer. If it fails, we return
``None``, telling Grok that the ``traverse()`` method didn't find the
object asked for. Grok then falls back on default behavior, which in
this case would mean a ``404 Not Found`` error.

Traversable attributes
~~~~~~~~~~~~~~~~~~~~~~

In some cases, you want to traverse to attributes or methods of your
``grok.Model``. This can be done easily using the ``grok.traversable``
directive::

  class Mammoth(grok.Model):
      grok.traversable('trunk')

      trunk = Trunk()

  class MammothView(grok.View):
      grok.context(Mammoth)

      def render(self):
          return "I'm a mammoth!"

Now, if traversing to http://localhost/mammoth/trunk , a Trunk()
object will be exposed at that URL.

Views
-----

Now that we have models and can build structures of them, we will need
to look at ways to actually present them to the user: views. So what
is a view? A view is a class that represents a model in some way. It
creates a user interface of some sort (typically HTML) for a model. A
single model can have more than one view. It looks like this::

  class Index(grok.View):
      grok.context(Application)

      def render(self):
          return "This is the application"

The ``grok.context`` bit in the class is an example of using a *Grok
directive*. If you use ``grok.context`` on a view class, it connects
the view to the class we give it. So in this case, ``Index`` is a view
for ``Application``. Note that if there is only a single model in the
module and you want your view to be associated with it, you can leave
out ``grok.context`` and the view will be associated with that model
by default. Many directives have such default behavior, allowing you
to leave them out of your code if you organize your code in a certain
way.

The default view for a model is called ``index``. You can specify
``index`` at the end of the URL, like this::

  http://localhost:8080/app/index

What happens when you go to this URL is that Grok instantiates the
``Index`` class, creating a ``Index`` instance. View instances have
a number of attributes by default:

  * ``context``, the model instance that the view is presenting.

  * ``request``, the current web request.

  * ``response``, an object representing the response sent to the
                  user.  Used less often.

``index`` views are special, as it's also fine not to add ``index`` at
the end, because the name ``index`` is the default::

  http://localhost:8080/app

You can also create views with different names::

  class Edit(grok.View):
      grok.context(Application)

      def render(self):
          return "This is the edit screen for the application"

Now you can go to this URL::

   http://localhost:8080/app/edit

The name of the view is the name of the view class, lowercased. This
is the default behavior: you can override this using the ``grok.name``
directive::

  class SomeImpossiblyLongClassName(grok.View):
      grok.context(Application)
      grok.name('edit')

      def render(self):
          return "This is the edit screen for the application"

Templates
~~~~~~~~~

In the previous examples, we used the ``render`` method to determine
what you actually see on a web page. For most views we don't want to
do that: we want to use a template to prepare presentation. Using a
template with a view is easy.  First create a directory
``<name>_templates``, where ``<name>`` is the the module that contains
the views. So, if you are developing in a module ``app.py``, you need
to create a subdirectory ``app_templates`` for templates in the same
directory as the ``app.py`` module.

You can then add templates to that directory with the same name as the
view class name (lowercase), with the ``.pt`` extension
appended. These templates follow the Zope Page Template (ZPT) rules,
though Grok can also be extended to support other template languages.

You could for instance have this view::

  class Index(grok.View):
      grok.context(Application)

and a file ``index.pt`` in the module's templates directory containing
template code.

These are the defaults. If for some reason you want the name of the
template directory not to be based on the name of module, you can
manually set the name of the template directory used by a module by
using the ``grok.templatedir`` directive in the module. If you want
the name of the template not to be based on the name of the class, you
use the ``grok.template`` directive in the view class.

The template can access attributes and methods on the view through the
special ``view`` name available in the template. The template can
access attributes and methods on the model through the special
``context`` name available in the template. The template has the
following special names available::

* ``view`` - the view that this template is associated with

* ``context`` - the model that is being viewed

* ``request`` - the current request object

* ``static`` - to make URLs to static content made available by this module

and any names you also make available using the ``namespace`` method.

static content
~~~~~~~~~~~~~~

A typical web page references one or more CSS files, javascript files
and images: static content that is part of the layout.

To make available static content to your template create a directory
in your package called ``static``. Put ``.css`` files, ``.js`` files,
image and whatever else is needed in there.

You can now refer to these static files in your template using the
special name ``static``, like this (ZPT example)::

  <img tal:attributes="src static/my_image.png" />

This will automatically create a URL to the place where Grok published
that image.

You can create subdirectories in ``static`` and refer to them as you'd
expect::

  <image tal:attributes="src static/images/some_image.gif" />

``update``
~~~~~~~~~~

You can define an ``update`` method in a view to prepare a view just
before it is accessed. You can use this to process information in the
request (URL parameters or form variables) or in the context, and set
attributes on the view that can be used in the template::

  def update(self):
      self.total = int(self.request.form['a']) + int(self.request.form['b'])

The template now has access to ``view.total``.

You can define parameters in the update view. These will be
automatically bound to parameters (or form values) in the request::

  def update(self, a, b):
      self.total = int(a) + int(b)

``namespace``
~~~~~~~~~~~~~

If you just want a variable to become available in the top-level of
your template (much like ``view`` and ``model``), you can also define
the ``namespace`` method on the view::

  def namespace(self):
      return {'foo': "Some value"}

You can now refer to ``foo`` in your template and have available to
this value.

the ``url`` method
~~~~~~~~~~~~~~~~~~

Views have a special method called ``url()`` that can be used to
create URLs to objects. The ``url`` method takes zero, one or two
arguments and an additional optional keyword argument 'data' that
is converted into a CGI query string appended to the URL::

* self.url() - URL to this view.

* self.url(object) - URL to the provided object.

* self.url(u"name") - URL to the context object, with ``/name`` appended,
                   to point to a view or subobject of the context.

* self.url(object, u"name") - URL to the provided object, with
  		   ``/name`` appended, to point to a view or subobject
  		   of the provided object.

* self.url(object, u"name", data={'name':'Peter', 'age':28})
            - URL to the provided object, with ``/name`` appended
              with '?name=Peter&age=28' at the end.

* self.url(data={'name':u'Andr\xe9', 'age:int':28}) - URL to the provided
                   object with '?name=Andre%C3%A9'&age%3Aint=28'.

From the view, this is accessed through ``self.url()``. From the
template, this method can be accessed using ``view.url()``.

the ``application_url`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using views it is sometimes desirable to be able to construct a
URL to the application object. ``application_url`` is a quick way to
do it.  It takes a single optional argument, name, which is the name
of a view of the application.

the ``redirect`` method
~~~~~~~~~~~~~~~~~~~~~~~

The ``redirect`` method on views can be used to redirect the browser
to another URL. Example::

   def render(self):
       self.redirect(self.url(self.context.__parent__))
       # return empty body as we are going to redirect anyway
       return ''

``__parent__`` and ``__name__`` on views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like models, views also get supplied with a ``__parent__`` and
``__name__`` object when they are instantiated for a particular model.

``__parent__`` points to the model being viewed (and is the same as
``context``, which should normally be used).

``__name__`` is the name of the view in the URL.

The ``@@`` thing
~~~~~~~~~~~~~~~~

Supposing you have a view called ``edit``, whenever you write this::

  http://localhost:8080/app/edit

you can also write this::

  http://localhost:8080/app/@@edit

Why the ugly ``@@`` syntax? Imagine that ``app`` is a container, and
that your user interface lets the user add objects to it with a name
of their own choosing. The user could decide to add an object called
``index``. In that case Grok wouldn't know whether the
``http://localhost:8080/app/index`` index is to get to a view or a
subobject. ``@@`` tells the system to look up a view definitely. If
``@@`` is not provided, subobjects take precedence over views in case
of name collision.

Request
-------

Some useful things to know about the request object (accessible as an
attribute on the view):

Information on the ``request`` object can be accessed using mapping
access (``request[`foo`]``). You can access request form variables and
cookies and headers (including `environment variables`_).

.. _`environment variables`: http://hoohoo.ncsa.uiuc.edu/cgi/env.html

To access form variables in particular use: ``request.form['foo']``.

To access cookies in particular use: ``request.cookies['foo']``.

To access headers (and environment variables) in particular use:
``request.headers['foo']``. You can also use ``request.getHeader()``,
with the header name as the argument, and an optional second default
argument.

Instead of the mapping access, the ``get`` methods work as well, as on
normal Python dictionaries.

More can be found in the ``IHTTPRequest`` interface documentation
in ``zope.publisher.interfaces.http``.

Response
--------

Some useful things to know about the response object (accessible as
an attribute on the view):

``setStatus(name, reason)`` sets the HTTP status code. The argument
may either be an integer representing the status code (such as ``200``
or ``400``), or a string (``OK``, ``NotFound``). The optional second
argument can be be used to pass the human-readable representation
(``Not Found``).

``setHeader(name, value)`` can be used to set HTTP response headers. The first
argument is the header name, the second the value.

``addHeader(name, value)`` can be used to add a HTTP header, while
retaining any previously set headers with the same name.

``setCookie(name, value, **kw)`` can be used to set a cookie. The first
argument is the cookie name, the second the value. Optional keyword
arguments can be used to set up further cookie properties (such as
``max_age`` and ``expires``).

``expireCookie(name, **kw)`` can be used to immediately expire a
cookie.

More can be found in the ``IHTTPResponse`` interface documentation
in ``zope.publisher.interfaces.http``.

Adapters
--------

An adapter is much like a view, but is aimed towards developers, not
end users. It presents an interface to an object, but an interface for
developers, not an user interface for end-users.

The section on adapters will of necessity be rather abstract. Feel
free to skip it until you want to know what is going on up with
interfaces and adapters - it is an important foundation to Grok, but one
you do not know much about when you get started.

An adapter can be used to add new methods to an object without
changing the object. To demonstrate the principle, we will construct
adapters entirely by hand first. At the end we will show how Groks
helps in constructing adapters and using them.

Imagine we are developing a content management system and we want to
get information about the size (in, say, bytes, approximately) of
content objects stored in our CMS, for instance in order to display it
in our UI or to calculate the total size of all objects in a
container. The simplest approach would be to add a ``size()`` method
to all our content objects::

  class Document(grok.Model):
       def __init__(self, text):
           self.text = text

       def size(self):
           return len(self.text.encode('UTF-8'))

  class Image(grok.Model):
       def __init__(self, data):
            self.data = data

       def size(self):
            return len(self.data)

  class Container(grok.Container):
        def size(self):
            total = 0
            for obj in self.values():
                total += obj.size()
            return total

For simple cases this is fine, but for larger applications this can
become a problem. Our ``Document`` model needs a ``size`` method, and
does our ``Image`` model, and our ``Container``, and our ``News Item``
model, and so on. Given the requirements of a typical CMS, content
objects would soon end up with a very large number of methods, for all
sorts of functionality, from getting the size of objects to offering a
commenting facility. It would be nicer to separate things out and keep
the underlying models clean.

To do this, we can use the adaptation pattern. As said, we will do it
by hand at first. An adapter is an object that adds an API to another
object (typically stored as the ``context`` attribute of the
adapter)::

  class DocumentSized(object):
      def __init__(self, context):
          self.context = context

      def size(self):
          return len(self.context.text.encode('UTF-8'))

We would use it like this::

   DocumentSized(document).size()

We could extend this same adapter to work for different kinds of
content objects, but that isn't very extensible when new adapters need
to be made::

  class Sized(object):
      def __init__(self, context):
          self.context = context

      def size(self):
          if isinstance(self.context, Document):
               return len(self.context.text.encode('UTF-8'))
          elif isinstance(self.context, Image):
               return len(self.context.data)
          elif isintance(self.context, Container):
               total = 0
               for obj in self.context.values():
                   total += Sized(obj).size()
               return total

Instead, we can create a smart ``sized`` factory that does this
switch-on-type behavior instead, keeping our adapters clean::

  class DocumentSized(object):
      def __init__(self, context):
          self.context = context

      def size(self):
          return len(self.context.text.encode('UTF-8'))

  class ImageSized(object):
      def __init__(self, context):
          self.context = context

      def size(self):
          return len(self.context.data)

  class ContainerSized(object):
      def __init__(self, context):
          self.context = context

      def size(self):
          total = 0
          for obj in self.context.values():
              total += sized(obj).size()
          return total

  def sized(context):
      if isinstance(context, Document):
          return DocumentedSized(context)
      elif isinstance(context, Image):
          return ImageSized(context)
      elif isinstance(context, Container):
          return ContainerSized(context)

We can now call ``sized`` for a content object and get an object back
that implements the "sized API"::

   s = sized(my_content_object)
   print s.size()

It's good to spell out the APIs of your application explicitly, as
documentation so that other developers can work with them and also
implement them for their own content objects. Grok lets you do this
using an *interface* specification, using the ``zope.interface``
package::

  from zope.interface import Interface

  class ISized(Interface):
      def size():
           "Return the size of the object"

We can now make this ``ISized`` interface into the adapter factory
(like ``sized`` above), without actually having to implement it
directly. Let's do that now by subclassing from ``grok.Adapter`` and
using a few grok directives::

  class DocumentSized(grok.Adapter):
      grok.context(Document)
      grok.provides(ISized)

      def size(self):
          return len(self.context.text.encode('UTF-8'))

  class ImageSized(grok.Adapter):
      grok.context(Image)
      grok.provides(ISized)

      def size(self):
          return len(self.context.data)

  class ContainerSized(grok.Adapter):
      grok.context(Container)
      grok.provides(ISized)

      def size(self):
          total = 0
          for obj in self.context.values():
              total += ISized(obj).size()
          return total

We can now use ``ISized`` like we used ``sized`` above::

   s = ISized(my_content_object)
   print s.size()

When new content objects were to be created for this CMS, ``ISized``
adapters can be registered for them anywhere. Using this pattern,
existing objects implemented by someone else can be made to conform
with the ``ISized`` API without having to modify them.

``grok.context`` works as for views. It is useful to point it to any
class however, not just that of models. ``grok.provides`` has to be
pointed to an interface (the interface that the adapter *adapts to*).

Interfaces
~~~~~~~~~~

Classes can also be made to *implement* an interface. This means that
instances of that class *provide* that interface::

  from zope.interface import Interface, Attribute

  class IAnimal(Interface):
      name = Attribute("The name of the animal")

      def makeSound():
          "The sound the animal makes."

  class Cow(object):
      grok.implements(IAnimal)

      def __init__(self, name):
          self.name = name

      def makeSound(self):
          return "Mooo"

We can ask the interface machinery whether an object provides an interface::

  >>> cow = Cow()
  >>> IAnimal.providedBy(cow)
  True

If you use an interface to adapt an object, and this object already
provides the interface, you get back the object itself::

  >>> IAnimal(cow) is cow
  True

``grok.context`` can always point to an interface instead of a class
directly. This indirection can be useful to make a view or adapter
work for a whole set of classes that all implement the same interface.

``ComponentLookupError``
~~~~~~~~~~~~~~~~~~~~~~~~

What if an adapter cannot be found for a particular object? Perhaps no
adapter has been registered for a particular object or a particular
interface. The system will raise a ``ComponentLookupError``::

  >>> ISized(cow)
  Traceback (most recent call last):
    ...
  ComponentLookupError

If you want to catch this exception, you can import it from
``zope.component.interfaces``::

  from zope.component.interfaces import ComponentLookupError

Named adapters
~~~~~~~~~~~~~~

It is possible to give an adapter a name, making it a *named
adapter*. This way it is possible to have more than one adapter
registered for a single object that all provide the same interface,
each with a different name. This feature is rarely used directly,
but internally it is used for views, as we will see later. The
``grok.name()`` directive can be used to give an adapter a name::

  class Adapter(object):
      grok.name('somename')
      grok.context(SomeClass)
      grok.provides(ISomeInterface)

Actually all adapters are named: by default the name of an adapter is
the empty string.

You cannot call the interface directly to get a named adapter for an
object.  Instead, you need to use the APIs provided by the
``zope.component`` package, in particular ``getAdapter``::

  from zope import component

  my_adapter = component.getAdapter(some_object, ISomeInterface,
                                   name='somename')

``getAdapter`` can also be used to look up unnamed adapters, as an
alternative to using the interface directly::

  myadapter = component.getAdapter(some_object, ISomeInterface)

Functions as adapters
~~~~~~~~~~~~~~~~~~~~~

Sometimes an adapter doesn't need to be a full-fledged class;
registering the factory function itself is enough. We can do this with
the ``@grok.adapter`` and ``@grok.implementer`` decorators. This way
we can write simple adapters that don't need to return a full-fledged
custom class instance but for instance some built-in Python object
like a string::

  @grok.adapter(SomeClass)
  @grok.implementer(ISomeInterface)
  def some_interface_for_some_class(some_instance):
      return str(some_instance)

You can now do the following::

  some_instance = SomeClass()
  s = ISomeInterface(some_instance)
  print s

``ISomeInterface`` now behaves much like ``str`` for ``SomeClass``.

Multi adapters
~~~~~~~~~~~~~~

Another feature of adapters is that you can adapt multiple objects at
once using a *multi adapter*. Again this feature is rarely used in
practice, except internally to implement views and events.

You can construct a multi adapter by subclassing from
``grok.MultiAdapter``::

  class MyMultiAdapter(grok.MultiAdapter):
      grok.adapts(SomeClass, AnotherClass)
      grok.provides(ISomeInterface)

      def __init__(some_instance, another_instance):
          self.some_interface = some_instance
          self.another_instance = another_instance

The multi-adapter receives as many arguments as what it was registered
for using ``grok.adapts``.

A multi adapter also cannot be looked up directly by calling the
interface. Instead, we need to use the ``zope.component`` package
again::

  from zope import component

  my_multi_adapter = component.getMultiAdapter((some_object, another_object),
                                               ISomeInterface)

``getMultiAdapter`` receives as the first argument a tuple with the
combination of objects to adapt.

It can also optionally be named using ``grok.name`` and then looked up
using a name argument::

  my_named_multi_adapter = component.getMultiAdapter(
      (some_object, another_object), ISomeInterface, name="foo")

Views as adapters
~~~~~~~~~~~~~~~~~

A view in Grok is in fact a named multi adapter, providing the base
interface (``Interface``). This means that a view in Grok can be
looked up in code by the following call::

  from zope.interface import Interface

  view = component.getMultiAdapter((object, request), Interface, name="index")

Since the default for the second argument is in fact ``Interface``, this
call can be shorted to this::

  view = component.getMultiAdapter((object, request), name="index")

Being able to do this in code is sometimes useful. It is also what
Grok does internally when it looks up a view.

Events
------

Grok lets you write handlers for *events*. Using event handlers you
can hook into code that you do not control. Events allow decoupling: a
framework can send events without worrying who is interested in it,
and similarly you can send events to work with existing bits of
framework that expects them. You can also define new types of events
if you are designing a framework yourself.

You write an event handler by writing a function that *subscribes* to
the event, and marking it with a python decorator::

  @grok.subscribe(Document, grok.IObjectAddedEvent)
  def handle(obj, event):
      print "Object %s was added." % obj

Whenever an instance of a model of class ``Document`` (or subclasses)
is added to a container, this code will be run. You can then take some
action. Any ``grok.Container`` subclass will take care of sending
these events automatically.  You can have as many subscribers for a
particular event as you like.  The order in which they are run is not
guaranteed by the system, so cannot be relied on.

The event handler takes two arguments: the object for which the event
was fired, and the event instance. The event instance has attributes,
depending on the type of event.

Events defined by Grok
~~~~~~~~~~~~~~~~~~~~~~

Here we describe the standard events defined by Grok. Described are
the interfaces which you would use in a subscriber, and how you can
send this event yourself. Other events may be defined by libraries or
by you.

``IObjectMovedEvent``
+++++++++++++++++++++

Will be fired whenever an object is moved from container to container,
renamed, added or removed.

The event object has these attributes:

* ``object`` - the object being moved

* ``oldParent`` - the parent (container) from which the object was moved
                  or removed, or ``None`` if this object is newly added.

* ``oldName`` - the previous name of the object in its container,
                before renaming if renaming took place, or ``None`` if
                this object is newly added.

* ``newParent`` - the parent (container) to this object was moved or
                added. ``None`` if this object was removed.

* ``newName`` - the name the object has in the new container, or ``None``
                if this object was removed.

Containers take care of sending this event, but should you want to
send it yourself, use::

  grok.notify(grok.ObjectMovedEvent(obj, oldParent, oldName, newParent, newName))

``IObjectAddedEvent``
+++++++++++++++++++++

Fired when an object is added to a container. Specialization of
``IObjectMovedEvent``, and shares the attributes as described.

Containers take care of sending this event, but should you want to send it
yourself, use::

  grok.notify(grok.ObjectAddedEvent(obj))

or::

  grok.notify(grok.ObjectAddedEvent(obj, newParent, newName))

``IObjectRemovedEvent``
+++++++++++++++++++++++

Fired when an object is removed from a container (and not re-added
elsewhere). Specialization of ``IObjectMovedEvent``, and shares the
attributes as described.

Containers take care of sending this event, but should you want to send it
yourself, use::

  grok.notify(grok.ObjectRemovedEvent(obj)

or::

  grok.notify(grok.ObjectRemovedEvent(obj, oldparent, oldName))

``IObjectModifiedEvent``
++++++++++++++++++++++++

Fired when an object is modified by the system, such as when a form is
saved. If you modify the object in code, the system won't know about
this, and you will have to remember to send it yourself.

This event has a single attribute, ``object``, which is the object
that was modified.

To send this event yourself, use::

  grok.notify(grok.ObjectModifiedEvent(obj))

``IContainerModifiedEvent``
+++++++++++++++++++++++++++

A specialization of ``IObjectModifiedEvent`` that fires when the
container was modified by adding something to it or removing from it.

Containers take care of sending this event, but if you want to send it
yourself, use::

  grok.notify(grok.ContainerModifiedEvent(obj))

``IObjectCreatedEvent``
+++++++++++++++++++++++

Fired when an object is created. When you create your own objects the
system won't know about this, and you will have to remember to send it
yourself if you care about listing to ``IObjectCreatedEvent``. This is
fairly rare - usually you're better of looking at
``IObjectAddedEvent`` if you can.

This event has a single attribute, ``object``, which is the object
that was created.

To send this event yourself::

  grok.notify(grok.ObjectCreatedEvent(obj))

``IObjectCopiedEvent``
++++++++++++++++++++++

Fired when an object was copied. It is a specialization of
``IObjectCreatedEvent`` that is fired by the system if you use the
``zope.copypastemove`` functionality.

Besides the ``object`` attribute it shares with
``IObjectCreattedEvent``, it has also has the ``original`` attribute,
which was the object that iwas copied from.

To send this event yourself::

  grok.notify(grok.ObjectCopiedEvent(copy, original))

``IBeforeTraverseEvent``
+++++++++++++++++++++++++

Fired when the publisher is about to traverse into your object. This
is useful to specify on your application object if you for instance
want to set the default skin for your application.

Creating and sending your own events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are going to send an object that pertains to a particular object,
subclass ``zope.component.interfaces.ObjectEvent``::

  from zope.component.interfaces import ObjectEvent

  class MyEvent(ObjectEvent):
      pass

You can then send it like this::

  grok.notify(MyEvent(some_obj))

And listen for it like this::

  @grok.subscribe(SomeClass, MyEvent)
  def handle_my_event(obj, event):
      pass

This subclassing from ``ObjectEvent`` is not required; if your event
isn't about an object, you can choose to design your event class
entirely yourself. See ``zope.sendmail`` for the construction of mail sending
events for an example.

Interfaces for events
~~~~~~~~~~~~~~~~~~~~~

For documentation purposes it can be a good idea to to define an
interface for your event. You can then also allow for multiple
implementations of the same event interface. When you have an
interface for your event, you can then listen for the interface in the
subscribers as well::

  from zope.interface import Interface

  class IMyEvent(zope.component.interfaces.IObjectEvent):
      "My special event"

  class MyEvent(zope.component.interfaces.ObjectEvent):
      grok.implements(IMyEvent)

  @grok.subscribe(SomeClass, IMyEvent):
  def handle_my_event(obj, event):
      pass

More about interfaces
---------------------

We have seen small examples of interfaces before, but here we will go
a bit more into them, and why they are useful.

An *interface* is a description of the API of a class (or more rarely,
module or object). Interfaces are useful because:

* They are API documentation.

* They can describe how a framework expects you to implement classes
  that fit into it.

* The system can inspect the interfaces a particular object provides,
  and treat them as an abstract form of classes for registration
  purposes.

Interfaces make it possible to use a generic framework's pluggability
points with confidence: you can clearly see what you are supposed to
implement to plug into it. You can define very generic frameworks
yourself by defining them in terms of interfaces.

Some interface features
~~~~~~~~~~~~~~~~~~~~~~~

A summary of interface features we've seen:

* To create an interface, subclass from ``zope.interface.Interface``.

* To state that implementors of the interface must have a method, supply
  the method with arguments. Don't use ``self`` as the first
  arguments, as this is an implementation detail not important to the
  interface. Instead, describe the methods as they look to the caller.

* To state that implementors of the interface must have an attribute, use::

    some_attribute = zope.interface.Attribute("Description of attribute")

* To state a class *implements* an interface, use ``grok.implements``.

* Instances of a class are said to *provide* the interface that the
  class *implements*.

* You can check whether an instance provides a certain interface by using
  ``some_interface.providedBy``::

     IObjectEvent.providedBy(NonSubclassEvent(some_obj))

Interfaces and events
~~~~~~~~~~~~~~~~~~~~~

Let's study interfaces some more in connection with
``IObjectModifiedEvent``. The ``IObjectModifiedEvent`` interface looks
like this::

  class IObjectModifiedEvent(zope.component.interfaces.IObjectEvent):
      """An object has been modified"""

This refers us to the ``IObjectEvent`` interface, which looks like
this::

  from zope import interface

  class IObjectEvent(interface.Interface):
      """An event related to an object.
      """

      object = interface.Attribute("The subject of the event.")

We therefore know that if we implement ``IObjectModifiedEvent``, we
must supply a single attribute, ``object``.

The following event handler for instances of ``SomeClass`` subscribes
to *any* event that provides ``IModifiedObjectEvent``::

   @grok.subscribe(SomeClass, IObjectModifiedEvent):
   def handle_event(obj, event):
       "Called when there is an IObjectModifiedEvent for SomeClass instances."

This handler will be called not only for subclasses of the
``grok.ObjectModifiedEvent`` class, but also for other, otherwise
unrelated classes that implement ``IObjectEvent``, such as this one::

  class NonSubclassObjectEvent(object):
      grok.implements(IObjectEvent)

      def __init__(self, object):
           self.object = object

So far we have only used interfaces for the second argument of the
event handler registration, but the principle also works for the first
argument. For example, to handle ``IObjectModifiedEvent`` events for
all kinds of containers, you can subscribe to
``zope.container.interfaces.IContainer`` objects::

  @grok.subscribe(IContainer, IObjectModifiedEvent):
  def handle_event(obj, event):
      "Called whenever any container is modified"

``zope.container.interfaces.IContainer`` defines the abstract
container API that all containers must provide, no matter how they are
implemented internally.

Interfaces and adapters
~~~~~~~~~~~~~~~~~~~~~~~

The same principle also works for adapters and ``grok.context``. You
can use ``grok.context`` with interfaces as well as with concrete
classes. To write an adapter that works for any kind of container, you
can write::

  from zope.container.interfaces import IContainer

  class SortedKeysAdapter(grok.Adapter):
      grok.context(IContainer)
      grok.provides(ISortedKeys)

      def sortedKeys(self):
          return sorted(self.context.keys())

Interfaces and views
~~~~~~~~~~~~~~~~~~~~

The same principle can also be used with ``grok.context`` in other
places, such as in views. This view is registered for all containers::

  from zope.container.interfaces import IContainer

  class Keys(grok.View):
     grok.context(IContainer)

     def render(self):
         return ', '.join(ISortedKeysAdapter(self.context).sortedKeys())

The view ``keys`` exists for all containers, no matter how they are
implement, where they are implemented or who implemented them, as long
as they provide ``IContainer``.

Using the fact ``Interface`` is the base of all interfaces, you can
even register a view for *all* objects. This can be useful to register
ZPT macros, which will then be available on all contexts::

  class Layout(grok.View):
      grok.context(Interface)

with a template ``layout.pt`` associated to it.

You can then use these macros in any page template anywhere by
referring to them like this::

  <html metal:use-macro="context/@@layout/macros/page">

Forms
-----

Grok can autogenerate web forms from descriptions called *schema*. A
schema is a special kind of interface. We already saw ``Attribute``,
which can be used to specify that something that provides that
interface should have that attribute. The ``zope.schema`` package adds
a lot more specific field descriptions. Here is an example of a
schema::

  from zope.interface import Interface
  from zope import schema

  class ISpecies(Interface):
      name = schema.TextLine(u"Animal species name")
      scientific_name = schema.TextLine(u"Scientific name")
      legs = schema.Int(u"Number of legs")

Let's also look at a simple implementation of this interface::

  class Species(grok.Model):
      grok.implements(ISpecies)

Note how we aren't even creating an ``__init__`` to set the
attributes; we could, but we'll see below that Grok's ``applyData``
can take care of this automatically.

The ``ISpecies`` schema can be turned into a form. Grok does this by
looking up a *widget* for each schema field to display it. A widget is
very much like a view. Let's look at a form for this schema::

  class Species(grok.Form):
      form_fields = grok.Fields(ISpecies)

      @grok.action(u"Save form")
      def handle_save(self, **data):
          print data['name']
          print data['scientific_name']
          print data['legs']

What is going on here? Firstly we use a special base class called
``grok.Form``. A form is a special kind of ``grok.View``, and
associates the same way (using ``grok.context``). A form expects two
things:

* a ``form_fields`` attribute. Above we see the most common way to construct
  this attribute, using ``grok.Fields`` on the interface.

* one or more actions. Actions are specified by using the
  ``@grok.action`` decorator. An action gets the fields filled in the
  form as keyword parameters, so ``**data`` in this case. We could
  also have specified the arguments we expected specifically.

Form widgets translate the raw HTML form input to Python objects, such
as (unicode) strings, integers and datetime objects, as specified by
schema fields. The schema fields can then be used to validate this
input further. Forms are self-submitting, and in case of a validation
error the form can render them in-line next to the fields.

We'll look at a lot of form features next.

``grok.AddForm``
~~~~~~~~~~~~~~~~

An add form is used to create a new object. Most forms are views of
the object that they are representing, but an add form is typically
associated a view of the container in which new objects are to be
added. Let's look at an example::

  class SpeciesContainer(grok.Container):
      pass

  class Add(grok.AddForm):
      grok.context(SpeciesContainer)

      form_fields = grok.Fields(ISpecies)

      @grok.action(u"Add species")
      def add_species(self, **data):
          # create a species instance
          species = Species()
          # assign the right attributes to fulfill ISpecies schema with
          # the form data
          self.applyData(species, **data)
          # stores the instance into the SpeciesContainer
          name = data['name']
          self.context[name] = species
          # redirect to the newly created object
          self.redirect(self.url(species))
          # we don't want to display anything, as we redirect
          return ''

The user can now go to ``myspeciescontainer/add`` to add a species,
where ``myspeciescontainer`` is any instance of ``SpeciesContainer``.

``grok.EditForm``
~~~~~~~~~~~~~~~~~

Now that we can create species objects, let's create a form so you can
easily edit them. This *is* a view of the ``Species`` model::

  class Edit(grok.EditForm):
     grok.context(Species)

     form_fields = grok.Fields(ISpecies)

     @grok.action(u"Edit species")
     def edit_species(self, **data):
          self.applyData(self.context, **data)

Forms are self-submitting, so this will show the edit form again. If
you want to display another page, you can redirect the browser as we
showed for the add form previously.

The user can now go to ``myspecies/edit`` to edit the species.

``grok.DisplayForm``
~~~~~~~~~~~~~~~~~~~~

Sometimes you just want to display an object, and not actually edit
it. If the object is schema-based, an easy way to do this is to use
display forms. Let's look at an example::

  class Display(grok.DisplayForm):
     grok.context(Species)

     form_fields = grok.Fields(ISpecies)

The user can now go to ``myspecies/display`` to look at the species.

Associating a template for a form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, Grok supplies some templates for forms. They work, but
they are not very pretty and don't fit into your application's
layout. You can instead use your own form rendering logic in a
template you associate with the form just like you associate templates
with views. You can also abstract form rendering logic you keep
reusing into a ZPT macro. Below is an example of form rendering logic
to help you get started. The example doesn't have any consideration
for layouting to make the logic clear. As a result, the form will be
very ugly if you use this - you will want to use CSS or table HTML to
layout things::

  <!-- render the form tag -->
  <form action="." tal:attributes="action request/URL" method="post"
        class="edit-form" enctype="multipart/form-data">
    <!-- render any validation errors on top -->
    <ul class="errors" tal:condition="view/errors">
      <li tal:repeat="error view/error_views">
         <span tal:replace="structure error">Error Type</span>
      </li>
    </ul>

    <!-- render the widgets -->
    <tal:block repeat="widget view/widgets">
      <label tal:attributes="for widget/name">
        <!-- a * when the widget is required -->
        <span class="required" tal:condition="widget/required">*</span>
        <!-- the title of the field -->
        <span i18n:translate="" tal:content="widget/label">label</span>
      </label>

      <!-- render the HTML widget -->
      <div class="widget" tal:content="structure widget">
        <input type="text" />
      </div>

      <!-- render any field specific validation error from a previous
           form submit next to the field -->
      <div class="error" tal:condition="widget/error">
        <span tal:replace="structure widget/error">error</span>
      </div>
    </tal:block>

    <!-- render all the action submit buttons -->
    <span class="actionButtons" tal:condition="view/availableActions">
      <input tal:repeat="action view/actions"
             tal:replace="structure action/render" />
    </span>
  </form>

The template for a display form a lot simpler::

  <tal:block repeat="widget view/widgets">
    <tal:block content="widget/label" />
    <input tal:replace="structure widget" />
  </tal:block>

  <!-- render all the action submit buttons -->
  <span class="actionButtons" tal:condition="view/availableActions">
    <input tal:repeat="action view/actions"
           tal:replace="structure action/render" />
  </span>
