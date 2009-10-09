
**********
Directives
**********

.. Here we document the generic behaviour of the module level and class level
   directives. The context sensitive behaviour is described in the individual
   component documentation. We do use specific example to illustrate the use
   of the directives.

The :mod:`grok` module defines a set of directives that allow you to configure
and register your components. Most directives assume a default, based on the
environment of a module. (For example, a view will be automatically associated
with a model if the association can be made unambigously.)

If no default can be assumed for a value, grok will explicitly tell you what
is missing and how you can provide a default or explicit assignment for
the value in question.

Core directives
~~~~~~~~~~~~~~~

Core directives are applicable to any type of component.

:func:`grok.name`
=================

Associate a component with a name.

Name is a unique identifier in the form of a string. The names of
Containers, Models and Views are used to compose the URLs of the application.

.. function:: grok.name(name)

    A class level directive used to associate a component with a single
    name `name`.

    Typically this directive is optional. The default behaviour when no
    name is given depends on the component. The same applies to the
    semantics of this directive: for what exactly a name is set when
    using this directive, depends on the component.

**Example: Specify the name of a View to make a more readable URL**

A common use case is to have a URL for a view named differently than
the name of the view class itself. In this example, the class is named
`SomeView` but is accessible at an URL suffixed with `/index`.

.. code-block:: python

    import grok

    class Mammoth(grok.Model):
      pass

    class SomeView(grok.View):
       grok.name('index')


.. seealso::

    :class:`grok.Adapter`, :class:`grok.Annotation`,
    :class:`grok.GlobalUtility`, :class:`grok.Indexes`,
    :class:`grok.MultiAdapter`, :class:`grok.Role`,
    :class:`grok.View`


:func:`grok.title`
==================

Succint description.

This directive is not commonly used, but along with :func:`grok.description`
can help provide more information about a component.

.. function:: grok.title(title)

   A descriptive title for a component.


:func:`grok.description`
========================

Longer description.

This directive is not commonly used, but along with :func:`grok.title`
can help provide more information about a component.

.. function:: grok.description(description)

  A longer description for a component.

 
:func:`grok.implements`
=======================

Declare that a class implements an interface.

.. function:: grok.implements(*interfaces)

    A class level directive to declare one or more `interfaces`, as
    implementers of the surrounding class.

    This directive allows several parameters.

    :func:`grok.implements` is currently an alias for
    :func:`zope.interface.implements`.

**Example: Create two Cave classes, one implements IPaintable the other does not**

First we will create the IPaintable interface, which declares that objects
which provide this interface will have a `paint()` method. We will make a
plain `Cave` class as well:

.. code-block:: python

    import grok
    from zope import interface
    
    class IPaintable(interface.Interface):
        def paint(color):
            "Paint with a color"

    class Cave(object):
        pass

You can create a `Cave` object and query the `IPaintable` interface to see if
an object provides that interface:

.. code-block:: python

    >>> cave = Cave()
    >>> IPaintable.providedBy(cave)
    False

Next we will make a `PaintableCave` class which does implement the
`IPaintable` interface:

.. code-block:: python

    class PaintableCave(object):
        grok.implements(IPaintable)

        def paint(color):
            self._painted_color = color

Now we can create a `PaintableCave` object and when we query the `IPaintable`
interface it asserts that the object does provide the interface:
    
    >>> paintable_cave = PaintableCave()
    >>> IPaintable.providedBy(paintable_cave)
    True

Note that interfaces, like all things in Python, are by nature of a 
"gentleman's agreement". It's possible to declare that an object provides
a certain interface when in reality it does not. It's also possible to
provide magic methods such as `__getattr__` to allow an object to conform
to a declared interface without that object needing to explicitly support
the concrete methods and attributes declared in the interface. You can
use the functions `zope.interface.verify.verifyClass(interface, class)`
and `zope.interface.verify.verifyObject(interface, object)` to verify if
a class or object actually implements or provides a specific interface.

:func:`grok.provides`
=====================

Disambiguate which interface is registered.

.. function:: grok.provides(interface)

    Explicitly specify with which interface a component will be
    looked up. If a class declares that it implements several interfaces,
    :func:`grok.provides` can be used to disambiguate which interface will be
    registered with the Zope Component Architecture.

.. seealso::

    :func:`grok.implements`


:func:`grok.direct`
===================

Specify that the class should be the component.

Typically a class implements an interface, and the class is used as a
factory to construct objects that provide that interface. With this
directive, the class object can by used to provide the interface
directly without constructing additional instance objects.

.. function:: grok.direct()

    Specify whether the class should be used for the component
    or whether it should be used to instantiate the component.

    This directive can be used on GlobalUtility-based classes to
    indicate whether the class itself should be registered as a
    utility, or an instance of it.


:func:`grok.baseclass`
======================

Declare a class as a base class.

.. function:: grok.baseclass()

    A class-level directive without argument to mark something as a base
    class. Base classes are not grokked.

    The baseclass mark is not inherited by subclasses, so those
    subclasses will be grokked (except if they are also explicitly declared as
    baseclasses as well).

**Example: Mark a View class as a Base Class**

Using this example, only the :class:`WorkingView` will serve as a
view, while calling the :class:`AnotherView` will lead to a
:exc:`ComponentLookupError`.

.. code-block:: python

    import grok

    class ModelBase(grok.Model):
        pass

    class AnotherView(grok.View):
        grok.baseclass()

        def render(self):
            return "hello world"

    class WorkingView(grok.View):
        pass


Utility directives
~~~~~~~~~~~~~~~~~~

:func:`grok.global_utility`
===========================

Register a global utility.

.. function:: grok.global_utility(factory[, provides=None[, name=u'']])

    A module level directive to register a global utility.

    `factory` - the factory that creates the utility.

    `provides` - the interface the utility should be looked up with.

    `name` - the name of the utility.

    The latter two parameters are optional.

    To register the utility correctly, Grok must be able to identify an
    interface provided by the utility. If none is given, Grok checks
    whether (exactly) one interface is implemented by the factory to be
    registered (see example below). If more than one interface is
    implemented by a class, use :func:`grok.provides` to specify which
    one to use. If no interface is implemented by the instances
    delivered by the factory, use :func:`grok.implements` to specify
    one.

    Another way to register global utilities with Grok is to subclass from
    :class:`grok.GlobalUtility`.

**Example: Register two GlobalUtilities and use them**

Given the following module code:

.. code-block:: python

    import grok
    from zope import interface

    class IFireplace(interface.Interface):
        pass

    class Fireplace(object):
        grok.implements(IFireplace)

    grok.global_utility(Fireplace)
    grok.global_utility(Fireplace, name='hot')

Then the following works:

.. code-block:: python

    from zope import component
    fireplace = component.getUtility(IFireplace)
    hot_fireplace = component.getUtility(IFireplace, name='hot')

.. seealso::

    :class:`grok.GlobalUtility`, :func:`grok.provides`,
    :func:`grok.implements`


:func:`grok.local_utility`
==========================

Register a local utility.

.. function:: grok.local_utility(factory[, provides=None[, name=u''[, setup=None[, public=False[, name_in_container=None]]]]])

    A class level directive to register a local utility.

    `factory` -- the factory that creates the utility.

    `provides` -- the interface the utility should be looked up with.

    `name` -- the name of the utility.

    `setup` -- a callable that receives the utility as its single
             argument, it is called after the utility has been created
             and stored.

    `public` -- if `False`, the utility will be stored below
              `++etc++site`.  If `True`, the utility will be stored
              directly in the site.  The site should in this case be a
              container.

    `name_in_container` -- the name to use for storing the utility.

    All but the first parameter are optional.

    To register a local utility correctly, Grok must know about the
    interface, the utility should be looked up with. If none is given,
    Grok looks up any interfaces implemented by instances delivered by
    `factory` and if exactly one can be found, it is taken. See
    :func:`grok.global_utility`.

    Every single combination of interfaces and names can only be
    registered once per module.

    It is not possible to declare a local utility as public, if the site
    is not a container. Grok will remind you of this. To store a utility
    in a container, a `name_in_container` is needed. If none is given,
    Grok will make up one automatically.

    An alternative way to define a local utility is to subclass from
    :class:`grok.LocalUtility`.

**Example: Register a local utility**

    The following code registers a local unnamed utility `fireplace` in
    instances of :class:`Cave`

    .. code-block:: python

      import grok
      from zope import interface

      class IFireplace(interface.Interface):
          pass

      class Fireplace(grok.LocalUtility):
          grok.implements(IFireplace)

      class Cave(grok.Container, grok.Site):
          grok.local_utility(Fireplace, public=True,
                             name_in_container='fireplace')

.. seealso::

    :func:`grok.global_utility`, :class:`grok.LocalUtility`

Adapter directives
~~~~~~~~~~~~~~~~~~

:func:`grok.context`
====================

Declare the context for views, adapters, etc.

Adapters are composed from another object, this object is called the
context object. This directive specifies the class or interface that
this object must provide.

If the context declaration is not supplied, then Grok will set the context
to the an Application, Container or Model class in module, as long as there
is only one class of that type in the module.

.. function:: grok.context(*class_or_interface)

    A class or module level directive to indicate the context for
    something (class or module) in the same scope.

    When used on module level, it will set the context for all views,
    adapters, etc. in that module. When used on class level, it will set
    the context for that particular class.

    With Grok contexts are set automatically for some objects, if they are
    unambigous. For example a :class:`grok.View` will get the only
    :class:`grok.Application` or :class:`grok.Model` class as context,
    iff there exists exactly one in the same module. If there are more
    possible contexts or you want to set a type (class/interface) from
    another module as context, than the one choosen by default, then you
    have to call :func:`grok.context` explicitly.

**Example: Declare a component depends upon a class or interface**

Here the :func:`grok.context` directive indicates that the :class:`Index`
View applies to the context of a :class:`Mammoth` instance, and not instances
of :class:`Cave`. By declaring the class or interface with :func:`grok.context`
for an object, you are stating that your object depends upon the methods
and attributes of that context.

.. code-block:: python

    import grok

    class Mammoth(grok.Model):
        hair = 'Wooly'

    class Cave(grok.Model):
        texture = 'rough'

    class Index(grok.View):
        grok.context(Mammoth)

        def render(self):
            # self.context will always have the interface of a Mammoth object,
            # since this view declares that it depends upon the context of a
            # Mammoth class.
            return "It feels %s" % self.context.hair

.. seealso::

    :class:`grok.View`, :class:`grok.Adapter`, :class:`grok.MultiAdapter`


:func:`grok.adapts`
===================

Declare that a class adapts certain objects.

In the case of a simple adapter which only requires a single object
for adapation, the :func:`grok.context` directive is used to declare
the interface or class the adapter is for. It is only necessary to use
:func:`grok.adapts` to declare the adapation requirements for a multi adapter.

.. function:: grok.adapts(*classes_or_interfaces)

    A class-level directive to declare that a class adapts objects of
    the classes or interfaces given in `\*classes_or_interfaces`.

    This directive accepts several arguments.

    It works much like the :mod:`zope.component.`:func:`adapts()`,
    but you do not have to make a ZCML entry to register the adapter.


Security directives
~~~~~~~~~~~~~~~~~~~

:func:`grok.require`
====================

Declare a permission.

.. function:: grok.require(permission)

A class level directive used to protect a View by requiring a
certain permission.

`permission` -- the class of the :class:`grok.Permission` subclass that
                is required. Alternatively, the name of the permission that is
                required


**Example 1 Define a Permission and use it to protect a View, using permission class**

.. code-block:: python

    import grok
    import zope.interface
    
    class Read(grok.Permission):
        grok.name('mypackage.Read')

    class Index(grok.View):
        grok.context(zope.interface.Interface)
        grok.require(Read)

**Example 2: Define a Permission and use it to protect a View, using permission name**

.. code-block:: python

    import grok
    import zope.interface
    
    class Read(grok.Permission):
        grok.name('mypackage.Read')

    class Index(grok.View):
        grok.context(zope.interface.Interface)
        grok.require('mypackage.Read')

.. seealso::

    :class:`grok.Permission` component, :func:`@grok.require` decorator


Component registry directives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`grok.site`
=================

Specify the local component registry to use for indexes.

A class level directive used in `grok.Indexes` sub-classes to define
in which local component registry the indexes should be located.

.. function:: grok.site(*arg)

**Example**

.. code-block:: python

    class MammothIndexes(grok.Indexes):
	grok.site(Herd)
	grok.context(IMammoth)

	name = index.Field()

View directives
~~~~~~~~~~~~~~~

:func:`grok.layer`
==================

Declare the layer for the view.

.. function:: grok.layer(layer)

    Declare the layer for the view.

    This directive acts as a contraint on the 'request' of
    grok.View. This directive can only be used on class level.


:func:`grok.skin`
=================

Declare this layer as a named skin.

.. function:: grok.skin(skin)

    Declare this layer as a named skin.

    This directive can only be used on class level.


:func:`grok.template`
=====================

Specify a template name.

A class level directive used to specify the template to be rendered
for the View when no render method is defined. This allows you to
override the default convention of naming the template file with the same
name as the view class itself, lowercased, in the templates directory
for this module.

.. function:: grok.template(template)

    `template` -- name of the template file without file extension

.. seealso::

    :func:`grok.templatedir`


:func:`grok.templatedir`
========================

Specify the templates directory.

A module level directive used to specify the directory where Grok
should look for template files.

The default convention is to look for template files in a directory
named `<module>_templates` where `<module>` is the name of the current
module.

.. function:: grok.templatedir(directory)

    `directory` -- the name of the directory inside the same package
                   as the module

.. seealso::

    :func:`grok.template`


:func:`grok.order`
==================

Specify ordering of components.

Ordering is typically used in Viewlets to determine the order in which 
they are displayed.

.. function:: grok.order(order)

    Control the ordering of components.

    If the value is specified, the order will be determined by sorting on it.
    If no value is specified, the order will be determined by definition
    order within the module. If the directive is absent, the order will be
    determined by class name.

    Inter-module order is by dotted name of the module the components are in,
    unless an explicit argument is specified to ``grok.order()``, components are
    grouped by module.

The function grok.util.sort_components can be used to sort
components according to these rules.


URL Traversal directives
~~~~~~~~~~~~~~~~~~~~~~~~

:func:`grok.traversable`
========================

Mark attributes or methods as traversable.

A class level directive used to mark attributes or methods as traversable. An
optional `name` argument can be used to give the attribute a different name in
the URL.

.. function:: grok.traversable(attr, name=None)

**Example**

.. code-block:: python

  class Foo(grok.Model):
      grok.traversable('bar')
      grok.traversable('foo')
      grok.traversable(attr='bar', name='namedbar')

      def __init__(self, name):
          self.name = name

      foo = Bar('foo')
      def bar(self):
          return Bar('bar')

The result is that you can now access http://localhost/foo/bar,
http://localhost/foo/foo and http://localhost/foo/namedbar.
