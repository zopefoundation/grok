
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

If no default can be assumed for a value, grok will explicitly tell you what is
missing and how you can provide a default or explicit assignment for the value
in question.

Core directives
~~~~~~~~~~~~~~~

:func:`grok.context` -- Declare the context for views, adapters, etc.
=====================================================================


.. function:: grok.context(*class_or_interface)

A class or module level directive to indicate the context for something
(class or module) in the same scope. When used on module level, it will set
the context for all views, adapters, etc. in that module. When used on class
level, it will set the context for that particular class.

With Grok contexts are set automatically for some objects, if they are
unambigous. For example a :class:`grok.View` will get the only
:class:`grok.Application` or :class:`grok.Model` class as context, iff there
exists exactly one in the same module. If there are more possible contexts
or you want to set a type (class/interface) from another module as context,
than the one choosen by default, then you have to call :func:`grok.context`
explicitly.

**Example:**

Here the :func:`grok.context` directive indicates, that
:class:`Mammoth` instances will be the context of :class:`Index`
views (and not instances of :class:`Cave`) ::

   import grok

   class Mammoth(grok.Model):
       pass

   class Cave(grok.Model):
       pass

   class Index(grok.View):
       grok.context(Mammoth)

.. seealso::

   :class:`grok.View`, :class:`grok.Adapter`, :class:`grok.MultiAdapter`

:func:`grok.name` -- associate a component with a name
======================================================

.. function:: grok.name(name)

A class level directive used to associate a component with a single name
`name`. Typically this directive is optional. The default behaviour when no
name is given depends on the component. The same applies to the semantics of
this directive: for what exactly a name is set when using this directive,
depends on the component.

**Example:** ::

   import grok

   class Mammoth(grok.Model):
      pass

   # a common use case is to have a URL for a view named differently than
   # the name of the view class itself.
   class SomeView(grok.View):
      grok.name('index')


.. seealso::

   :class:`grok.Adapter`, :class:`grok.Annotation`,
   :class:`grok.GlobalUtility`, :class:`grok.Indexes`,
   :class:`grok.MultiAdapter`, :class:`grok.Role`,
   :class:`grok.View`

:func:`grok.title`
========================

.. function:: grok.title(*arg)

   foobar

:func:`grok.implements` -- indicate, that a class implements an interface
=========================================================================

.. function:: grok.implements(*interfaces)

A class level directive to declare one or more `interfaces`, as implementers
of the surrounding class. This directive allows several parameters.

:func:`grok.implements` is currently an alias for
:func:`zope.interface.implements`.

**Example:** ::

   >>> import grok
   >>> from zope import interface
   >>> class IPaintable(interface.Interface):
   ...   pass
   ...
   >>> class Cave(object):
   ...   pass
   ...
   >>> cave = Cave()
   >>> IPaintable.providedBy(cave)
   False
   >>> class PaintableCave(object):
   ...   grok.implements(IPaintable)
   ...
   >>> cave = PaintableCave()
   >>> IPaintable.providedBy(cave)
   True

:func:`grok.provides`
=====================

.. function:: grok.provides(interface)

If the component implements more than one interface, :func:`grok.provides`
is required to disambiguate for what interface the component will be
registered.

.. seealso::

   :func:`grok.implements`

:func:`grok.adapts` -- Declare that a class adapts certain objects
==================================================================

.. function:: grok.adapts(*classes_or_interfaces)

A class-level directive to declare that a class adapts objects of the
classes or interfaces given in `\*classes_or_interfaces`.

This directive accepts several arguments.

It works much like the :mod:`zope.component`\ s :func:`adapts()`, but you do
not have to make a ZCML entry to register the adapter.

**Example:** ::

   import grok
   from zope import interface, schema
   from zope.size.interfaces import ISized

   class IMammoth(interface.Interface):
       name = schema.TextLine(title=u"Name")
       size = schema.TextLine(title=u"Size", default=u"Quite normal")

   class Mammoth(grok.Model):
       interface.implements(IMammoth)

   class MammothSize(object):
       grok.implements(ISized)
       grok.adapts(IMammoth)

       def __init__(self, context):
           self.context = context

       def sizeForSorting(self):
           return ('byte', 1000)

       def sizeForDisplay(self):
           return ('1000 bytes')

Having :class:`MammothSize` available, you can register it as an adapter,
without a single line of ZCML::

   >>> manfred = Mammoth()
   >>> from zope.component import provideAdapter
   >>> provideAdapter(MammothSize)
   >>> from zope.size.interfaces import ISized
   >>> size = ISized(manfred)
   >>> size.sizeForDisplay()
   '1000 bytes'

.. seealso::

   :func:`grok.implements`

:func:`grok.baseclass` -- declare a class as base
=================================================

.. function:: grok.baseclass()

A class-level directive without argument to mark something as a base class.
Base classes are are not grokked.

Another way to indicate that something is a base class, is by postfixing the
classname with ``'Base'``.

The baseclass mark is not inherited by subclasses, so those subclasses will
be grokked (except they are explicitly declared as baseclasses as well).

**Example:** ::

   import grok

   class ModelBase(grok.Model):
       pass

   class ViewBase(grok.View):
       def render(self):
           return "hello world"

   class AnotherView(grok.View):
       grok.baseclass()

       def render(self):
           return "hello world"

   class WorkingView(grok.View):
       pass

Using this example, only the :class:`WorkingView` will serve as a view,
while calling the :class:`ViewBase` or :class:`AnotherView` will lead to a
:exc:`ComponentLookupError`.

Utility directives
~~~~~~~~~~~~~~~~~~

:func:`grok.global_utility` -- register a global utility
========================================================

.. function:: grok.global_utility(factory[, provides=None[, name=u'']])

A module level directive to register a global utility.

`factory` - the factory that creates the utility.

`provides` - the interface the utility should be looked up with.

`name` - the name of the utility.

The latter two parameters are optional.

To register the utility correctly, Grok must be able to identify an
interface provided by the utility. If none is given, Grok checks whether
(exactly) one interface is implemented by the factory to be registered (see
example below). If more than one interface is implemented by a class, use
:func:`grok.provides` to specify which one to use. If no interface is
implemented by the instances delivered by the factory, use
:func:`grok.implements` to specify one.

Another way to register global utilities with Grok is to subclass from
:class:`grok.GlobalUtility`.

**Example:**

   Given the following module code: ::

      import grok
      from zope import interface

      class IFireplace(interface.Interface):
          pass

      class Fireplace(object):
          grok.implements(IFireplace)

      grok.global_utility(Fireplace)
      grok.global_utility(Fireplace, name='hot')

   Then the following works: ::

      >>> from zope import component
      >>> fireplace = component.getUtility(IFireplace)
      >>> IFireplace.providedBy(fireplace)
      True
      >>> isinstance(fireplace, Fireplace)
      True

      >>> fireplace = component.getUtility(IFireplace, name='hot')
      >>> IFireplace.providedBy(fireplace)
      True
      >>> isinstance(fireplace, Fireplace)
      True

.. seealso::

   :class:`grok.GlobalUtility`, :func:`grok.provides`,
   :func:`grok.implements`

:func:`grok.local_utility` -- register a local utility
======================================================

.. function:: grok.local_utility(factory[, provides=None[, name=u''[, setup=None[, public=False[, name_in_container=None]]]]])

A class level directive to register a local utility.

`factory` -- the factory that creates the utility.

`provides` -- the interface the utility should be looked up with.

`name` -- the name of the utility.

`setup` -- a callable that receives the utility as its single
   argument, it is called after the utility has been created and
   stored.

`public` -- if `False`, the utility will be stored below
   `++etc++site`.  If `True`, the utility will be stored directly
   in the site.  The site should in this case be a container.

`name_in_container` -- the name to use for storing the utility.

All but the first parameter are optional.

To register a local utility correctly, Grok must know about the interface,
the utility should be looked up with. If none is given, Grok looks up any
interfaces implemented by instances delivered by `factory` and if exactly
one can be found, it is taken. See :func:`grok.global_utility`.

Every single combination of interfaces and names can only be registered once
per module.

It is not possible to declare a local utility as public, if the site is not
a container. Grok will remind you of this. To store a utility in a
container, a `name_in_container` is needed. If none is given, Grok will make
up one automatically.

An alternative way to define a local utility is to subclass from
:class:`grok.LocalUtility`.

**Example:**

   The following code registers a local unnamed utility `fireplace` in
   instances of :class:`Cave` ::

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

:func:`grok.resourcedir --- XXX Not implemented yet`
====================================================

.. function:: grok.resourcedir(*arg)

   foobar

Resource directories are used to embed static resources like HTML-,
JavaScript-, CSS- and other files in your application.

XXX insert directive description here (first: define the name, second:
describe the default behaviour if the directive isn't given)

A resource directory is created when a package contains a directory with the
name :file:`static`. All files from this directory become accessible from a
browser under the URL
:file:`http://<servername>/++resource++<packagename>/<filename>`.

**Example:**

The package :mod:`a.b.c` is grokked and contains a directory :file:`static`
which contains the file :file:`example.css`. The stylesheet will be
available via :file:`http://<servername>/++resource++a.b.c/example.css`.

.. note::

A package can never have both a :file:`static` directory and a Python module
with the name :file:`static.py` at the same time. grok will remind you of
this conflict when grokking a package by displaying an error message.

Linking to resources from templates
-----------------------------------

grok provides a convenient way to calculate the URLs to static resource using
the keyword :keyword:`static` in page templates::

<link rel="stylesheet" tal:attributes="href static/example.css" type="text/css">

The keyword :keyword:`static` will be replaced by the reference to the resource
directory for the package in which the template was registered.

Security directives
~~~~~~~~~~~~~~~~~~~

:func:`grok.require`
====================

.. function:: grok.require(permission)

A class level directive used to protect a View by requiring a certain permission. 

`permission` -- the name of the permission that is required

** Example **::

	class ViewPainting(grok.Permission):
	    grok.name('grok.ViewPainting')
	

.. seealso::

  :class:`grok.Permission` component, :func:`@grok.require` decorator


Template directives
~~~~~~~~~~~~~~~~~~~

:func:`grok.template`
=====================

.. function:: grok.template(template)

A class level directive used to specify the template to be rendered for the View when no render method is defined.

`template` -- name of the template file

** Convention **

When not specified, Grok will look for a template file with the same name as the view class itself, lowercased, in the templates directory for this module.

.. seealso::

   :func:`grok.templatedir`

:func:`grok.templatedir`
========================

A module level directive used to specify the directory where Grok should look for template files.

.. function:: grok.templatedir(directory)

`directory` -- the name of the directory inside the same package as the module

** Convention **

When not specified, Grok will look template files in a diretory named `<module>_templates` where `<module>` is the name of the current module.

.. seealso::

   :func:`grok.template`

Uncategorized directives
~~~~~~~~~~~~~~~~~~~~~~~~

:func:`grok.site`
=================

.. function:: grok.site(*arg)

A class level directive used in `grok.Indexes` sub-classes to define in which local component registry the indexes should be located.

** Example **
::

	class MammothIndexes(grok.Indexes):
	    grok.site(Herd)
	    grok.context(IMammoth)

	    name = index.Field()
