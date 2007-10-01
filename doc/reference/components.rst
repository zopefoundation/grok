
**********
Components
**********

The :mod:`grok` module defines a set of components that provide basic Zope 3
functionality in a convenient way.


:class:`grok.Adapter`
=====================

Implementation, configuration, and registration of Zope 3 adapters.


.. class:: grok.Adapter

   Base class to define an adapter. Adapters are automatically registered when a
   module is "grokked".


   .. attribute:: grok.Adapter.context

      The adapted object.

   **Directives:**

   :func:`grok.context(context_obj_or_interface)`
      Maybe required. Identifies the type of objects or interface for the adaptation.

      If Grok can determine a context for adaptation from the module, this directive
      can be omitted. If the automatically determined context is not correct, or if no
      context can be derived from the module the directive is required.

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interface(s) the adapter implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If ommitted, no
      name will be used.

      When a name is used for the adapter registration, the adapter can only be
      retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the adapter implements more than one interface,
      :func:`grok.provides` is required to disambiguate for what interface the adapter
      will be registered.

**Example:** ::

   import grok
   from zope import interface

   class Cave(grok.Model):
       pass

   class IHome(interface.Interface):
       pass

   class Home(grok.Adapter):
       grok.implements(IHome)

   home = IHome(cave)

**Example 2:** ::

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


:class:`grok.AddForm`
=====================


:class:`grok.Annotation`
========================


:class:`grok.Application`
=========================


grok.ClassGrokker
=================


:class:`grok.Container`
=======================


.. class:: grok.Container

   Mixin base class to define a container object. The container implements the
   zope.app.container.interfaces.IContainer interface using a BTree, providing
   reasonable performance for large collections of objects.


:class:`grok.DisplayForm`
=========================


:class:`grok.EditForm`
======================


:class:`grok.Form`
==================


:class:`grok.GlobalUtility`
===========================


.. class:: grok.GlobalUtility

   Base class to define a globally registered utility. Global utilities are
   automatically registered when a module is "grokked".

   **Directives:**

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interfaces(s) the utility implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If ommitted, no
      name will be used.

      When a name is used for the global utility registration, the global utility can
      only be retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the global utility implements more than one interface,
      :func:`grok.provides` is required to disambiguate for what interface the global
      utility will be registered.


:class:`grok.Indexes`
=====================


grok.InstanceGrokker
====================


:class:`grok.JSON`
==================


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
      Optional. Identifies the name used for the adapter registration. If ommitted, no
      name will be used.

      When a name is used for the local utility registration, the local utility can
      only be retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the local utility implements more than one interface or if
      the implemented interface cannot be determined, :func:`grok.provides` is
      required to disambiguate for what interface the local utility will be
      registered.


.. seealso::

   Local utilities need to be registered in the context of :class:`grok.Site` or
   :class:`grok.Application` using the :func:`grok.local_utility` directive.


:class:`grok.Model`
===================

Base class to define an application "content" or model object. Model objects
provide persistence and containment.


grok.ModuleGrokker
==================


:class:`grok.MultiAdapter`
==========================


.. class:: grok.MultiAdapter

   Base class to define a multi adapter. MultiAdapters are automatically registered
   when a module is "grokked".

   **Directives:**

   :func:`grok.adapts(\*objects_or_interfaces)`
      Required. Identifies the combination of types of objects or interfaces for the
      adaptation.

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interfaces(s) the adapter implements.

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If ommitted, no
      name will be used.

      When a name is used for the adapter registration, the adapter can only be
      retrieved by explicitely using its name.

   :func:`grok.provides(name)`
      Maybe required. If the adapter implements more than one interface,
      :func:`grok.provides` is required to disambiguate for what interface the adapter
      will be registered.

**Example:** ::

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


grok.PageTemplate
=================


grok.PageTemplateFile
=====================


:class:`grok.Site`
==================

Base class to define an site object. Site objects provide persistence and
containment.


:class:`grok.Traverser`
=======================


:class:`grok.View`
==================


:class:`grok.XMLRPC`
====================

