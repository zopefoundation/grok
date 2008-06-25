
**********
Components
**********

.. Here we documented the component base classes. For the directive possible
   for each component we document only the specific within its context. We then
   refer to the directives documented in the directives.rst file.

The :mod:`grok` module defines a set of base classes for creating new 
components of different types, that provide basic Zope 3 functionality in a convenient way. Grok applications are built by subclassing these components.

Components in Grok and Zope 3 can be any plain Python object, that you have declared implements one or more Interface(s). The inclusion of these Grok base classes in your own Python classes inheritance automatically handles the component registration with the Zope Component Architecture. This process of introspecting your Grok code during initialization and wiring together components based on common conventions that you follow in the structure of your source code is called "grokking".


Core components
~~~~~~~~~~~~~~~

:class:`grok.Application`
=========================

Base class for applications. Inherits from :class:`grok.Site`.

:class:`grok.Model`
===================

Base class to define an application "content" or model object. Model objects
provide persistence and containment.

:class:`grok.Container`
=======================

Mixin base class to define a container object. Objects in a container are 
manipulated using the same syntax as you would with the standard
Python Dictionary object. The container implements the
zope.app.container.interfaces.IContainer interface using a BTree, providing
reasonable performance for large collections of objects.

**Example 1: Perform Create, Read, Update and Delete (CRUD) on a container**

.. code-block:: python

    # define a container and a model and then create them
    class BoneBag(grok.Container): pass
    class Bone(grok.Model): pass    
    bag = BoneBag()
    skull = Bone()
    
    # ... your classes are then "grokked" by Grok ...
    
    # store an object in a container
    bag['bone1'] = skull
    
    # test for containment
    bag.has_key('bone1')
    
    # retrieve an object from a container
    first_bone = bag['bone1'] 
    
    # iterate through objects in a container with .values()
    # you can also use .keys() and .items()
    for bone in bag.values():
        bone.marks = 'teeth'
    
    # delete objects using the del keyword
    del bag['bone1']

:class:`grok.Indexes`
=====================

Base class for catalog index definitions.

Adapters
~~~~~~~~

:class:`grok.Adapter`
=====================

Implementation, configuration, and registration of Zope 3 Adapters.

Adapters are components that are constructed from other components. They
take an existing interface and extend it to provide a new interface.

.. class:: grok.Adapter

   Base class to define an adapter. Adapters are automatically
   registered when a module is "grokked".

   .. attribute:: grok.Adapter.context

      The adapted object.

   **Directives:**

   :func:`grok.context(context_obj_or_interface)`
      Maybe required. Identifies the type of objects or interface for
      the adaptation.

   .. seealso::

      :func:`grok.context`

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interface(s) the adapter implements.

   .. seealso::

      :func:`grok.implements`

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter
      registration. If ommitted, no name will be used.

      When a name is used for the adapter registration, the adapter
      can only be retrieved by explicitely using its name.

   .. seealso::

      :func:`grok.name`

   :func:`grok.provides(name)`
      Maybe required.

   .. seealso::

      :func:`grok.provides`

**Example 1: Simple adaptation example**

.. code-block:: python

   import grok
   from zope import interface

   class Cave(grok.Model):
      "start with a cave objects (the adaptee)"

   class IHome(interface.Interface):
      "we want to extend caves with the IHome interface"

   class Home(grok.Adapter):
      "the home adapter turns caves into habitable homes!"
      grok.implements(IHome)

   # Adapation (component look-up) is invoked by passing the adaptee
   # to the interface as a constructor and returns the component adapted to   
   home = IHome(cave)


**Example 2: Register and retrieve the adapter under a specific name**

.. code-block:: python

   import grok
   from zope import interface

   class Cave(grok.Model):
      pass
   class IHome(interface.Interface):
      pass

   class Home(grok.Adapter):
      grok.implements(IHome)
      grok.name('home')

   from zope.component import getAdapter
   home = getAdapter(cave, IHome, name='home')


:class:`grok.MultiAdapter`
==========================

.. class:: grok.MultiAdapter

   Base class to define a Multi Adapter.
   
   A simple adapter normally adapts only one object, but an adapter may
   adapt more than one object. If an adapter adapts more than one objects,
   it is called multi-adapter.

   **Directives:**

   :func:`grok.adapts(\*objects_or_interfaces)`
      Required. Identifies the combination of types of objects or interfaces
      for the adaptation.

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interfaces(s) the adapter implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If
      ommitted, no name will be used.

      When a name is used for the adapter registration, the adapter can only be
      retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Only required if the adapter implements more than one interface.
      :func:`grok.provides` is required to disambiguate for which interface the
      adapter will be registered for.

**Example: A home is made from a cave and a fireplace.**

.. code-block:: python

   import grok
   from zope import interface

   class Fireplace(grok.Model):
       pass

   class Cave(grok.Model):
       pass

   class IHome(interface.Interface):
       pass

   class Home(grok.MultiAdapter):
       grok.adapts(Cave, Fireplace)
       grok.implements(IHome)

       def __init__(self, cave, fireplace):
           self.cave = cave
           self.fireplace = fireplace

   home = IHome(cave, fireplace)

:class:`grok.Annotation`
========================

Annotation components are persistent writeable adapters.

.. class:: grok.Annotation

   Base class to declare an Annotation. Inherits from the
   persistent.Persistent class.

**Example: Storing annotations on model objects**

.. code-block:: python

   import grok
   from zope import interface

   # Create a model and an interface you want to adapt it to
   # and an annotation class to implement the persistent adapter.
   class Mammoth(grok.Model):
      pass

   class ISerialBrand(interface.Interface):
      unique = interface.Attribute("Brands")

   class Branding(grok.Annotation):
      grok.implements(IBranding)
      unqiue = 0
   
   # Grok the above code, then create some mammoths
   manfred = Mammoth()
   mumbles = Mammoth()
   
   # creating Annotations work just like Adapters
   livestock1 = ISerialBrand(manfred)
   livestock2 = ISerialBrand(mumbles)
   
   # except you can store data in them, this data will transparently persist
   # in the database for as long as the object exists
   livestock1.serial = 101
   livestock2.serial = 102

Utilities
~~~~~~~~~

:class:`grok.GlobalUtility`
===========================

.. class:: grok.GlobalUtility

   Base class to define a globally registered utility. Global utilities are
   automatically registered when a module is "grokked".

   **Directives:**

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interfaces(s) the utility implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If
      ommitted, no name will be used.

      When a name is used for the global utility registration, the global
      utility can only be retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the global utility implements more than one interface,
      :func:`grok.provides` is required to disambiguate for what interface the
      global utility will be registered.


:class:`grok.LocalUtility`
==========================

.. class:: grok.LocalUtility

   Base class to define a utility that will be registered local to a
   :class:`grok.Site` or :class:`grok.Application` object by using the
   :func:`grok.local_utility` directive.

   **Directives:**

   :func:`grok.implements(\*interfaces)`
      Optional. Identifies the interfaces(s) the utility implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If
      ommitted, no name will be used.

      When a name is used for the local utility registration, the local utility
      can only be retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the local utility implements more than one interface
      or if the implemented interface cannot be determined,
      :func:`grok.provides` is required to disambiguate for what interface the
      local utility will be registered.

  .. seealso::

    Local utilities need to be registered in the context of :class:`grok.Site`
    or :class:`grok.Application` using the :func:`grok.local_utility` directive.

:class:`grok.Site`
==================

Views
~~~~~

:class:`grok.View`
==================

View components provide context and request attributes. 

The determination of what View gets used for what Model is made by walking the URL in the HTTP Request object sepearted by the / character. This process is
called Traversal.

.. class:: grok.View

   Base class to define a View.

   .. attribute:: grok.View.context

      The object that the view is presenting. This is often an instance of
      a grok.Model class, but can also be a grok.Application or grok.Container
      object.

   .. attribute:: grok.View.request
   
      The HTTP Request object.

   .. attribute:: grok.View.response

      The HTTP Response object that is associated with the request.

   .. attribute:: grok.View.static

      Directory resource containing the static files of the view's package.

   .. method:: redirect(url):
   
      Redirect to given URL

   .. method:: url(obj=None, name=None, data=None):
   
      Construct URL.

      If no arguments given, construct URL to view itself.

      If only obj argument is given, construct URL to obj.

      If only name is given as the first argument, construct URL
      to context/name.

      If both object and name arguments are supplied, construct
      URL to obj/name.

      Optionally pass a 'data' keyword argument which gets added to the URL
      as a cgi query string.

   .. method:: default_namespace():

      Returns a dictionary of namespaces that the template
      implementation expects to always be available.

      This method is *not* intended to be overridden by application
      developers.

   .. method:: namespace():
   
      Returns a dictionary that is injected in the template
      namespace in addition to the default namespace.

      This method *is* intended to be overridden by the application
      developer.

   .. method:: update(**kw):
   
      This method is meant to be implemented by grok.View
      subclasses.  It will be called *before* the view's associated
      template is rendered and can be used to pre-compute values
      for the template.

      update() can take arbitrary keyword parameters which will be
      filled in from the request (in that case they *must* be
      present in the request).

   .. method:: render(**kw):
   
      A view can either be rendered by an associated template, or
      it can implement this method to render itself from Python.
      This is useful if the view's output isn't XML/HTML but
      something computed in Python (plain text, PDF, etc.)

      render() can take arbitrary keyword parameters which will be
      filled in from the request (in that case they *must* be
      present in the request).

   .. method:: application_url(name=None):
   
      Return the URL of the closest application object in the
      hierarchy or the URL of a named object (``name`` parameter)
      relative to the closest application object.

   .. method:: flash(message, type='message'):
      
      Send a short message to the user.

:class:`grok.JSON`
==================

:class:`grok.XMLRPC`
====================

:class:`grok.Traverser`
=======================

:class:`grok.PageTemplate`
==========================

:class:`grok.PageTemplateFile`
==============================

Forms
~~~~~

:class:`grok.Form`
==================

.. Do not forget about the form_fields class attribute!

:class:`grok.AddForm`
=====================

:class:`grok.EditForm`
======================

:class:`grok.DisplayForm`
=========================

Security
~~~~~~~~

:class:`Permission`
===================

:func:`grok.define_permission` -- define a permission
=====================================================

.. function:: grok.define_permission(name)

   A module-level directive to define a permission with name
   `name`. Usually permission names are prefixed by a component- or
   application name and a dot to keep them unique.

   Because in Grok by default everything is accessible by everybody,
   it is important to define permissions, which restrict access to
   certain principals or roles.

   **Example:**

   .. code-block:: python

      import grok
      grok.define_permission('cave.enter')


   .. seealso::

      :func:`grok.require`, :class:`grok.Permission`, :class:`grok.Role`

   .. versionchanged:: 0.11

      replaced by :class:`grok.Permission`.

:class:`Role`
=============
