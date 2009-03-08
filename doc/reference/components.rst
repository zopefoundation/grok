
**********
Components
**********

.. Here we documented the component base classes. For the directive possible
    for each component we document only the specific within its context. We then
    refer to the directives documented in the directives.rst file.

The :mod:`grok` module defines a set of base classes for creating new 
components of different types, that provide basic Zope 3 functionality in a
convenient way. Grok applications are built by subclassing these components.

Components in Grok and Zope 3 are any plain Python object, that declare they
provide one or more Interface(s). The inclusion of these Grok base
classes in your own class inheritance automatically handles the
component registration with the Zope Component Architecture. This process of
introspecting your Grok code during initialization and wiring together
components based on common conventions that you follow in the structure
of your source code is called "grokking".


Core components
~~~~~~~~~~~~~~~

:class:`grok.Application`
=========================

Applications are top-level objects. They are typically used to hold global
configuration and behaviour for an application instance, as well as holding
data objects such as :class:`grok.Container` and :class:`grok.Model` object
instances.

When a new Grok application is installed using the Grok Admin interface, it
creates an instance of the :class:`grok.Application` class and saves it in
the root of the main ZODB database.

.. class:: grok.Application

    Base class for applications. Inherits from :class:`grok.Site`.


:class:`grok.Model`
===================

Model objects provide persistence and containment. Model in Grok refers to
an applications data model - that is data which is persistently saved to
disk, by default in the Zope Object Dataabse (ZODB).

.. class:: grok.Model

    Base class to define a content or model object.

    .. attribute:: __parent__

       The parent in the location hierarchy.
       
       If you recursively follow the `__parent__` attribute, you will always
       reach a reference to a top-level grok.Application object instance.

    .. attribute:: __name__
    
        The name within the parent.
        
        Traverse the parent with this name to get the object.

        Name in Grok means "human-readable identifier" as the `__name__`
        attribute is used to reference the object within an URL.


:class:`grok.Container`
=======================

Objects in a container are manipulated using the same syntax as you would
with a standard Python Dictionary object. The container implements the
zope.app.container.interfaces.IContainer interface using a BTree, providing
reasonable performance for large collections of objects.

.. class:: grok.Container

    Base class to define a container object.

    .. attribute:: __parent__

       The parent in the location hierarchy.
       
       If you recursively follow the `__parent__` attribute, you will always
       reach a reference to a top-level grok.Application object instance.

    .. attribute:: __name__
    
        The name within the parent.
        
        Traverse the parent with this name to get the object.

        Name in Grok means "human-readable identifier" as the `__name__`
        attribute is used to reference the object within an URL.

    .. method:: items(key=None)
    
        Return an iterator over the key-value pairs in the container.

        If ``None`` is passed as `key`, this method behaves as if no argument
        were passed.

        If `key` is in the container, the first item provided by the iterator
        will correspond to that key.  Otherwise, the first item will be for
        the key that would come next if `key` were in the container.

    .. method:: keys(key=None)
    
        Return an iterator over the keys in the container.

        If ``None`` is passed as `key`, this method behaves as if no argument
        were passed.

        If `key` is in the container, the first key provided by the iterator
        will be that key.  Otherwise, the first key will be the one that would
        come next if `key` were in the container.

    .. method:: values(key=None)
    
        Return an iterator over the values in the container.

        If ``None`` is passed as `key`, this method behaves as if no argument
        were passed.

        If `key` is in the container, the first value provided by the iterator
        will correspond to that key.  Otherwise, the first value will be for
        the key that would come next if `key` were in the container.


    .. method:: __getitem__(key)
        
        Get a value for a key

        A KeyError is raised if there is no value for the key.

    .. method:: get(key, default=None)
        
        Get a value for a key

        The default is returned if there is no value for the key.

    .. method:: __contains__(key)
        
        Tell if a key exists in the mapping.


    .. method:: __iter__()
    
        Return an iterator for the keys of the mapping object.

    .. method:: values()
        
        Return the values of the mapping object.

    .. method:: items()
        
        Return the items of the mapping object.

    .. method:: __len__()
        
        Return the number of items.

    .. method:: has_key(key)
    
        Tell if a key exists in the mapping.
    
    .. method:: __setitem__(name, object)
        
        Add the given `object` to the container under the given name.

        Raises a ``TypeError`` if the key is not a unicode or ascii string.
        Raises a ``ValueError`` if key is empty.

        The container might choose to add a different object than the
        one passed to this method.

        If the object doesn't implement `IContained`, then one of two
        things must be done:

        1. If the object implements `ILocation`, then the `IContained`
           interface must be declared for the object.

        2. Otherwise, a `ContainedProxy` is created for the object and
           stored.

        The object's `__parent__` and `__name__` attributes are set to the
        container and the given name.

        If the old parent was ``None``, then an `IObjectAddedEvent` is
        generated, otherwise, an `IObjectMovedEvent` is generated.  An
        `IContainerModifiedEvent` is generated for the container.

        If the object replaces another object, then the old object is
        deleted before the new object is added, unless the container
        vetos the replacement by raising an exception.

        If the object's `__parent__` and `__name__` were already set to
        the container and the name, then no events are generated and
        no hooks.  This allows advanced clients to take over event
        generation.

    .. method:: __delitem__(name)
        
        Delete the named object from the container.

        Raises a ``KeyError`` if the object is not found.

        If the deleted object's `__parent__` and `__name__` match the
        container and given name, then an `IObjectRemovedEvent` is
        generated and the attributes are set to ``None``. If the object
        can be adapted to `IObjectMovedEvent`, then the adapter's
        `moveNotify` method is called with the event.

        Unless the object's `__parent__` and `__name__` attributes were
        initially ``None``, generate an `IContainerModifiedEvent` for the
        container.

        If the object's `__parent__` and `__name__` were already set to
        ``None``, then no events are generated.  This allows advanced
        clients to take over event generation.


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


:class:`grok.OrderedContainer`
==============================

OrderedContainers act just like Containers, but also support the ability
to maintain order on the items within the container. This implementation
maintains a persistent list of keys on a private attribute, so it's 
important to note that OrderedContainers will have poorer performance than
a normal Container.

.. class:: grok.OrderedContainer

    Base class for an OrderedContainer. OrderedContainer inherits from
    Container and supports the same interface.
    
    .. method:: updateOrder(order)
    
        Revise the order of keys, replacing the current ordering.

        order is a list or a tuple containing the set of existing keys in
        the new order. `order` must contain ``len(keys())`` items and cannot
        contain duplicate keys.

        Raises ``TypeError`` if order is not a tuple or a list.

        Raises ``ValueError`` if order contains an invalid set of keys.


:class:`grok.Indexes`
=====================

Indexes are containers for holding a set of indexes. An index is 
a data structures that provides a way of quickly finding a data objects.
A single index can be of either `Field`, `Text`, or `Set`.

.. class:: grok.Indexes

    Base class for catalog index definitions.

**Example 1: Index the Mammoths in a Herd**

Imagine you have a herd of mammoths, and you wish to quickly find a 
mammoth based on their last name. First we will create a simple Grok
application that defines a Herd and some Mammoths:

.. code-block:: python

    import grok
    from zope.interface import Interface
    from zope import schema

    class Herd(grok.Container, grok.Application):
        pass

    class IMammoth(Interface):
        name = schema.TextLine(title=u'Full Name')

    class MammothIndexes(grok.Indexes):
        grok.site(Herd)
        grok.context(IMammoth)

        full_name = grok.index.Text()

    class Mammoth(grok.Model):
        grok.implements(IMammoth)

        def __init__(self, full_name):
            self.full_name = full_name

We can now create a Herd application, add some Mammoths to the Herd, and
query for those Mammoths by their last name:

.. code-block:: python

    # imagine herd is an already created Herd application instance
    herd['one'] = Mammoth('Manfred Mammoth')
    herd['two'] = Mammoth('Joe Mammoth')
    herd['three'] = Mammoth('Marty the Wooly')

    from zope.app.catalog.interfaces import ICatalog
    from zope.component import getUtility
    catalog = getUtility(ICatalog)
    mammoths = catalog.searchResults(full_name='Mammoth')
    # mammoths would be a list containing 'Manfred Mammoth' and 'Joe Mammoth'
    # but not 'Marty the Wooly'


Adapters
~~~~~~~~

:class:`grok.Adapter`
=====================

An Adapter takes an object providing an existing interface and extends
it to provide a new interface.

The object providing the existing interface is passed to the Adapter
in the constructor, and is stored in an attribute named 'context.
The source code for the `grok.Adapter` base class is simply:

.. code-block:: python

    class Adapter(object):
        def __init__(self, context):
            self.context = context

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
        "Cave is the class being adapted (the adaptee)"

        def __init__(self, size=100):
            self.size = size
    
    class IHome(interface.Interface):
        "IHome is the interface we want to add to a Cave"
        
        def renovate():
            "Enlarge Cave"
    
    class CaveHome(grok.Adapter):
        "Turns a Cave into a Home"
        grok.context(Cave) 
        grok.implements(IHome) # the new interface provided by the adapter

        def renovate(self):
            # the adaptee is an attribute named 'context'
            # and is passed in to the constructor
            self.context.size += 10

    # Adapation (component look-up) is invoked by passing the adaptee
    # to the interface as a constructor and returns the component adapted to   
    home = IHome(cave)
    home.renovate()
    
    # Multiple adapters can exist that adapt and provide the same interfaces.
    # They can be distinguished by name.
    
    import zope.component
    
    class LargeCaveHome(grok.Adapater):
        "Turns a Cave in a large Home"
        grok.context(Cave) 
        grok.implements(IHome)
        grok.name('largehome')
        
        def renovate(self):
            self.context.size += 200

    largehome = zope.component.getAdapter(cave, IHome, name='largehome')
    largehome.renovate()

:class:`grok.MultiAdapter`
==========================

A MultiAdapter takes multiple objects providing existing interface(s)
and extends them to provide a new interface.

The `grok.MultiAdapter` base class does not provide a default constructor
implementation, it's up to the individual multi-adapters to determine how
to handle the objects being adapted.

.. class:: grok.MultiAdapter

    Base class to define a Multi Adapter.

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
    import zope.component
    import zope.interface

    class Fireplace(grok.Model): pass
    class Cave(grok.Model): pass
    class IHome(zope.interface.Interface): pass

    class Home(grok.MultiAdapter):
        grok.adapts(Cave, Fireplace)
        grok.implements(IHome)

        def __init__(self, cave, fireplace):
            self.cave = cave
            self.fireplace = fireplace

    home = zope.component.getMultiAdapter((cave, fireplace), IHome)

**Example: A Grok View is a MultiAdapter**

In Grok, MultiAdapters are most commonly encountered in the form of
Views. A View is a MultiAdapter which adapts the `request` and the
`context` to provide the `IGrokView` interface. You can lookup a
View component using the `getMultiAdapter` function.

.. code-block:: python

    def FireplaceView(grok.View):
        grok.context(Fireplace)
        grok.name('fire-view')
    
    def AlternateFireplaceView(grok.View):
        grok.context(Fireplace)
        
        def render(self):
            fireplaceview = zope.component.getMultiAdapter(
                (self.context, self.request), IGrokView, name='fire-view'
            )
            return fireplaceview.render()


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
        unique = 0
   
    # Grok the above code, then create some mammoths
    manfred = Mammoth()
    mumbles = Mammoth()
   
    # creating Annotations work just like Adapters
    livestock1 = ISerialBrand(manfred)
    livestock2 = ISerialBrand(mumbles)
   
    # except you can store data in them, this data will transparently persist
    # in the database for as long as the object exists
    livestock1.unique = 101
    livestock2.unique = 102

    # attributes not listed in the interface will also be persisted
    # on the annotation
    livestock2.foo = "something"

Utilities
~~~~~~~~~

:class:`grok.GlobalUtility`
===========================

A global utility is an object which provides an interface, and can be
looked-up by that interface and optionally the component name. The
attributes provided by a global utility are not persistent.

Examples of global utilities are database connections, XML parsers,
and web service proxies.

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

A local utility is an object which provides an interface, and can be 
looked-up by that interface and optionally the component name. The attributes
provided by a local utility are transparently stored in the database (ZODB).
This means that configuration changes to a local utility lasts between
server restarts.

An example is for database connections or web service proxies, 
where you need to dynamically provide the connection settings
so that they can be edited through-the-web.

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

Contains a Site Manager. Site Managers act as containers for registerable
components.

If a Site Manager is asked for an adapter or utility, it checks for those
it contains before using a context-based lookup to find another site
manager to delegate to. If no other site manager is found they defer to
the global site manager which contains file based utilities and adapters.

.. class:: grok.Site

	.. method:: getSiteManager()

		Returns the site manager contained in this object.

		If there isn't a site manager, raise a component lookup.

	.. method:: setSiteManager(sitemanager)
	
		Sets the site manager for this object.

Views
~~~~~

:class:`grok.View`
==================

Views handle interactions between the user and the model. The are constructed
with context and request attributes, are responsible for providing a
response. The request attribute in a View will always be for a normal
HTTP Request.

The determination of what View gets used for what Model is made by walking the
URL in the HTTP Request object sepearted by the / character. This process is
called Traversal.

.. class:: grok.View

    Base class to define a View.
    
    Implements the `grokcore.view.interfaces.IGrokView` interface.

    .. attribute:: context

        The object that the view is presenting. This is often an instance of
        a grok.Model class, but can be a grok.Application, grok.Container
        object or any type of Python object.

    .. attribute:: request
   
        The HTTP Request object.

    .. attribute:: response

        The HTTP Response object that is associated with the request. This
        is also available as self.request.response, but the response attribute
        is provided as a convenience.

    .. attribute:: static

        Directory resource containing the static files of the view's package.

    .. method:: redirect(url)
   
        Redirect to given URL

    .. method:: url(obj=None, name=None, data=None)
   
        Construct URL.

        If no arguments given, construct URL to view itself.

        If only obj argument is given, construct URL to obj.

        If only name is given as the first argument, construct URL
        to context/name.

        If both object and name arguments are supplied, construct
        URL to obj/name.

        Optionally pass a 'data' keyword argument which gets added to the URL
        as a cgi query string.

    .. method:: default_namespace()

        Returns a dictionary of namespaces that the template
        implementation expects to always be available.

        This method is *not* intended to be overridden by application
        developers.

    .. method:: namespace()
   
        Returns a dictionary that is injected in the template
        namespace in addition to the default namespace.

        This method *is* intended to be overridden by the application
        developer.

    .. method:: update(**kw)
   
        This method is meant to be implemented by grok.View
        subclasses.  It will be called *before* the view's associated
        template is rendered and can be used to pre-compute values
        for the template.

        update() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request).

    .. method:: render(**kw)
   
        A view can either be rendered by an associated template, or
        it can implement this method to render itself from Python.
        This is useful if the view's output isn't XML/HTML but
        something computed in Python (plain text, PDF, etc.)

        render() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request).

    .. method:: application_url(name=None)
   
        Return the URL of the closest application object in the
        hierarchy or the URL of a named object (``name`` parameter)
        relative to the closest application object.

    .. method:: flash(message, type='message')
      
        Send a short message to the user.


:class:`grok.ViewletManager`
============================

A ViewletManager is a component that provides access to a set of
content providers (Viewlets). The ViewletManager's responsibilities are:

  * Aggregation of all viewlets registered for the manager.

  * Apply a set of filters to determine the availability of the viewlets.

  * Sort the viewlets based on some implemented policy. The default is to
    numerically sort accoring to the `grok.order([number])` directive on a
    Viewlet.

  * Provide an environment in which the viewlets are rendered.

  * Render itself containing the HTML content of the viewlets.

ViewletManager's also implement a read-only mapping API, so the Viewlet's
that they contain can be read like a normal Python dictionary.

.. class:: grok.ViewletManager

    Base class for a ViewletManager.
    
    .. attribute:: context

        Typically the Model object for which this ViewletManager is being
        rendered in the context of.
        
    .. attribute:: request
    
        The Request object.
    
    .. attribute:: view
    
        Reference to the View that the ViewletManager is being provided in.

    .. method::  update()

        This method is called before the ViewletManager is rendered, and
        can be used to perfrom pre-computation.
    
    .. method:: render(*args, **kw)

        This method renders the content provided by this ViewletManager.
        Typically this will mean rendering and concatenating all of the
        Viewlets managed by this ViewletManager.

**Example: Register a ViewletManager and Viewlet and use them from a template for a View**

This is a very simple example, ViewletManagers and Viewlets can be used to
support more complex HTML layout use cases, such as discriminating on the
view or context in which a particular ViewletManager will be rendered. For
example, a web site about caves and herds might want to show information in
the sidebar specific to either a cave or a herd, depending upon whether a page
is displaying information about a cave or a herd.

.. code-block:: python

    class ViewForACave(grok.View):
        def render():
            return grok.PageTemplate("""
            <html><body>
                <div tal:content="structure provider:cave" />
            </body></html>
            """)
    
    class CaveManager(grok.ViewletManager):
        grok.view(ViewForACave)
        grok.name('cave')

    class CaveViewlet(grok.Viewlet):
        grok.order(30)
        grok.viewletmanager(CaveManager)

        def render(self):
            return "Cave"


:class:`grok.Viewlet`
=====================

Viewlets are a flexible way to compound HTML snippets.

Viewlets are typically used for the layout of the web site. Often all the
pages of the site have the same layout with header, one or two columns, the
main content area and a footer.

.. class:: grok.Viewlet

    Base class for a Viewlet.

    .. attribute:: context

        Typically the Model object for which this Viewlet is being
        rendered in the context of.
    
    .. attribute:: request
    
        The Request object.
    
    .. attribute:: view
    
        Reference to the View that the Viewlet is being provided in.

    .. attribute:: viewletmanager
    
        Reference to the ViewletManager that is rendering this Viewlet.
    
    .. method::  update()

        This method is called before the Viewlet is rendered, and
        can be used to perfrom pre-computation.

    .. method:: render(*args, **kw)

        This method renders the content provided by this Viewlet.


:class:`grok.JSON`
==================

Specialized View that returns data in JSON format.

Python data returned is automatically converted into JSON format using
the simplejson library. Every method name in a grok.JSON component is
registered as the name of a JSON View. The exceptions are names that
begin with an _ or special names such as __call__. The grok.require
decorator can be used to protect methods with a permission.

.. class:: grok.JSON

    Base class for JSON methods.

**Example 1: Create a public and a protected JSON view.**

.. code-block:: python

    class MammothJSON(grok.JSON):
        """
        Returns JSON from URLs in the form of:
      
        http://localhost/stomp
        http://localhost/dance
        """

        grok.context(zope.interface.Interface)

        def stomp(self):
            return {'Manfred stomped.': ''}

        @grok.require('zope.ManageContent')
        def dance(self):
            return {'Manfred does not like to dance.': ''}


:class:`grok.REST`
==================

Specialized View for making web services that conform to the REST style.
These Views can define methods named GET, PUT, POST and DELETE, which will
be invoked based on the Request type.

.. class:: grok.REST

    Base class for REST.
    
    .. attribute:: context
    
        Object that the REST handler presents.

    .. attribute:: request
    
        Request that REST handler was looked up with.
    
    .. attribute:: body
    
        The text of the request body.


:class:`grok.XMLRPC`
====================

Specialized View that responds to XML-RPC.

.. class:: grok.XMLRPC

    Base class for XML-RPC methods.

**Example 1: Create a public and a protected XML-RPC view.**

The grok.require decorator can be used to protect methods with a permission.

.. code-block:: python

    import grok
    import zope.interface
    
    class MammothRPC(grok.XMLRPC):
        grok.context(zope.interface.Interface)

        def stomp(self):
            return 'Manfred stomped.'

        @grok.require('zope.ManageContent')
        def dance(self):
            return 'Manfred doesn\'t like to dance.'


:class:`grok.Traverser`
=======================

A Traverser is used to map from a URL to an object being published (Model)
and the View used to interact with that object.

.. class:: grok.Traverser

    Base class for custom traversers. Override the traverse method to 
    supply the desired custom traversal behaviour.

    .. attribute:: context

        The object that is being traversed.

    .. attribute:: request
   
        The HTTP Request object.

    .. method:: traverse(self, name):
      
        You must provide your own implementation of this method to do what
        you want. If you return None, Grok will use the default traversal
        behaviour.

    .. method:: browserDefault(request):
   
        Returns an object and a sequence of names.
	  
        The publisher calls this method at the end of each traversal path.
        If the sequence of names is not empty, then a traversal step is made
        for each name. After the publisher gets to the end of the sequence,
        it will call browserDefault on the last traversed object.
	  
        The default behaviour in Grok is to return self.context for the object
        and 'index' for the default view name.
	  
        Note that if additional traversal steps are indicated (via a
        nonempty sequence of names), then the publisher will try to adjust
        the base href.

    .. method:: publishTraverse(request, name):

        Lookup a name and return an object with `self.context` as it's parent.
        The method can use the request to determine the correct object.
	  
        The 'request' argument is the publisher request object. The
        'name' argument is the name that is to be looked up. It must
        be an ASCII string or Unicode object.
	  
        If a lookup is not possible, raise a NotFound error.

**Example 1: Traverse into a Herd Model and return a Mammoth Model**

.. code-block:: python

    import grok

    class Herd(grok.Model):

       def __init__(self, name):
           self.name = name

    class HerdTraverser(grok.Traverser):
       grok.context(Herd)

       def traverse(self, name):
           return Mammoth(name)

    class Mammoth(grok.Model):

       def __init__(self, name):
           self.name = name


:class:`grok.PageTemplate`
==========================

Page Templates are the default templating system for Grok, they are an
implementation of the Template Attribute Language (TAL). Page Templates
are typically created from a string.

.. code-block:: python

    grok.PageTemplate("<h1>Hello World!</h1>")

.. class:: grok.PageTemplate

    .. method:: _initFactory(factory)
    
        Template language specific initializations on the view factory.

    .. method:: render(view)
        
        Renders the template


:class:`grok.PageTemplateFile`
==============================

Creates a Page Template from a filename.

.. code-block:: python

    grok.PageTemplateFile("my_page_template.pt")

.. class:: grok.PageTemplateFile

    .. method:: _initFactory(factory)

        Template language specific initializations on the view factory.

    .. method:: render(view)
        
        Renders the template


Forms
~~~~~

Forms inherit from the `grok.View` class. They are a specialized type of
View that renders an HTML Form.

:class:`grok.Form`
==================

.. class:: grok.Form

    Base class for forms.

    .. attribute:: prefix
    
        Page-element prefix. All named or identified page elements in a
        subpage should have names and identifiers that begin with a subpage
        prefix followed by a dot.

    .. method:: setPrefix(prefix):

        Update the subpage prefix

    .. attribute:: label
    
        A label to display at the top of a form.
        
    .. attribute:: status
    
        An update status message. This is normally generated by success or
        failure handlers.
    
    .. attribute:: errors

        Sequence of errors encountered during validation.

    .. attribute:: form_result
    
        Return from action result method.

    .. attribute:: form_reset
    
        Boolean indicating whether the form needs to be reset.

    .. attribute:: form_fields
    
        The form's form field definitions.

        This attribute is used by many of the default methods.

    .. attribute:: widgets
    
        The form's widgets.

        - set by setUpWidgets

        - used by validate


    .. method:: setUpWidgets(ignore_request=False):
    
        Set up the form's widgets.

        The default implementation uses the form definitions in the
        form_fields attribute and setUpInputWidgets.

        The function should set the widgets attribute.

    .. method:: validate(action, data):
    
        The default form validator

        If an action is submitted and the action doesn't have it's own
        validator then this function will be called.

    .. attribute:: template
    
        Template used to display the form

    .. method:: resetForm():
    
        Reset any cached data because underlying content may have changed.

    .. method:: error_views():
    
        Return views of any errors.

        The errors are returned as an iterable.

    .. method:: applyData(obj, **data):
    
        Save form data to an object.

        This returns a dictionary with interfaces as keys and lists of
        field names as values to indicate which fields in which
        schemas had to be changed in order to save the data.  In case
        the method works in update mode (e.g. on EditForms) and
        doesn't have to update an object, the dictionary is empty.

:class:`grok.AddForm`
=====================

Add forms are used for creating new objects. The widgets for this form
are not bound to any existing content or model object.

.. class:: grok.AddForm

    Base class for add forms. Inherits from :class:`grok.Form`.

:class:`grok.EditForm`
======================

Edit forms are used for editing existing objects. The widgets for this form
are bound to the object set in the `context` attribute.

.. class:: grok.EditForm

    Base class for edit forms. Inherits from :class:`grok.Form`.

:class:`grok.DisplayForm`
=========================

Display forms are used to display an existing object. The widgets for this
form are bound to the object set in the `context` attribute.

.. class:: grok.DisplayForm

    Base class for display forms. Inherits from :class:`grok.Form`.


Security
~~~~~~~~

:class:`grok.Permission`
========================

Permissions are used to protect Views so that they can only be called by
an authenticated principal. If a View in Grok does not have a `grok.require`
directive declaring a permission needed to use the View, then the default
anonymously viewable `grok.Public` permission used.

.. class:: grok.Permission

    Base class for permissions. You must specify a unique name for every
    permission using the `grok.name` directive. The convention for ensuring
    uniqueness is to prefix your permission name with the name of your
    Grok package followed by a dot, e.g. 'mypackage.MyPermissionName'.

    .. attribute:: id
    
        Id as which this permission will be known and used. This is set
        to the value specified in the `grok.name` directive.

    .. attribute:: title

        Human readable identifier for this permission.

    .. attribute:: description

        Description of the permission.

    **Directives:**

    :func:`grok.name(name)`
    
        Required. Identifies the unique name (also used as the id) of the
        permission.

    :func:`grok.title(title)`

        Optional. Stored as the title attribute for this permission.
    
    :func:`grok.description(description)`

        Optional. Stored as the description attribute for this permission.

**Example 1: Define a new Permission and use it to protect a View**

.. code-block:: python

    import grok
    import zope.interface
    
    class Read(grok.Permission):
        grok.name('mypackage.Read')

    class Index(grok.View):
        grok.context(zope.interface.Interface)
        grok.require('mypackage.Read')


:class:`grok.Role`
==================

Roles provide a way to group together a collection of permissions. Principals
(aka Users) can be granted a Role which will allow them to access all Views
protected by the Permissions that the Role contains.

.. class:: grok.Role

    Base class for roles.

    .. attribute:: id
    
        Id as which this role will be known and used. This is set
        to the value specified in the `grok.name` directive.

    .. attribute:: title

        Human readable identifier for this permission.

    .. attribute:: description

        Description of the permission.

    **Directives:**

    :func:`grok.name(name)`

        Required. Identifies the unique name (also used as the id) of the
        role.

    :func:`grok.permissions(permissions)`

        Required. Declare the permissions granted to this role.

    :func:`grok.title(title)`

        Optional. Stored as the title attribute for this role.

    :func:`grok.description(description)`

        Optional. Stored as the description attribute for this role.

**Example 1: Define a new 'paint.Artist' Role and assign it to the 'paint.grok' principal**

.. code-block:: python

    import grok
    import zope.interface

    class ViewPermission(grok.Permission):
        grok.name('paint.ViewPainting')

    class EditPermission(grok.Permission):
        grok.name('paint.EditPainting')

    class ErasePermission(grok.Permission):
        grok.name('paint.ErasePainting')

    class ApprovePermission(grok.Permission):
        grok.name('paint.ApprovePainting')

    class Artist(grok.Role):
        """
        An Artist can view, create and edit paintings. However, they can
        not approve their painting for display in the Art Gallery Cave.
        """
        grok.name('paint.Artist')
        grok.title('Artist')
        grok.description('An artist owns the paintings that they create.')
        grok.permissions(
            'paint.ViewPainting', 'paint.EditPainting', 'paint.ErasePainting')

    class CavePainting(grok.View):
        grok.context(zope.interface.Interface)
        grok.require(ViewPermission)

        def render(self):
            return 'What a beautiful painting.'

    class EditCavePainting(grok.View):
        grok.context(zope.interface.Interface)
        grok.require(EditPermission)

        def render(self):
            return 'Let\'s make it even prettier.'

    class EraseCavePainting(grok.View):
        grok.context(zope.interface.Interface)
        grok.require(ErasePermission)

        def render(self):
            return 'Oops, mistake, let\'s erase it.'

    class ApproveCavePainting(grok.View):
        grok.context(zope.interface.Interface)
        grok.require(ApprovePermission)

        def render(self):
            return 'Painting owners cannot approve their paintings.'

    # The app variable will typically be your Application instance,
    # but could also be a container within your application.
    from zope.securitypolicy.interfaces import IPrincipalRoleManager
    IPrincipalRoleManager(app).assignRoleToPrincipal(
       'paint.Artixt', 'paint.grok')
