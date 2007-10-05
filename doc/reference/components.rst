
**********
Components
**********

.. Here we documented the component base classes. For the directive possible
   for each component we document only the specific within its context. We then
   refer to the directives documented in the directives.rst file.

The :mod:`grok` module defines a set of components that provide basic Zope 3
functionality in a convenient way. Grok applications are built by subclassing
these components.

Core components
~~~~~~~~~~~~~~~

:class:`grok.Model`
===================

Base class to define an application "content" or model object. Model objects
provide persistence and containment.

:class:`grok.Container`
=======================

Mixin base class to define a container object. The container implements the
zope.app.container.interfaces.IContainer interface using a BTree, providing
reasonable performance for large collections of objects.

:class:`grok.Application`
=========================

Adapters
~~~~~~~~

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

   .. seealso::

      :function:`grok.context`

   :func:`grok.implements(\*interfaces)`
      Required. Identifies the interface(s) the adapter implements.

   .. seealso::

      :function:`grok.implements`

   :func:`grok.name(name)`
      Optional. Identifies the name used for the adapter registration. If ommitted, no
      name will be used.

      When a name is used for the adapter registration, the adapter can only be
      retrieved by explicitely using its name.

   .. seealso::

      :function:`grok.name`

   :func:`grok.provides(name)`
      Maybe required.

   .. seealso::

      :function:`grok.provides`

**Example 1:** ::

   import grok
   from zope import interface

   class Cave(grok.Model):
       pass

   class IHome(interface.Interface):
       pass

   class Home(grok.Adapter):
       grok.implements(IHome)

   home = IHome(cave)

**Example 2: Register and retrieve the adapter under a specific name** ::

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

   Base class to define a multi adapter. MultiAdapters are automatically
   registered when a module is "grokked".

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
      Maybe required. If the adapter implements more than one interface,
      :func:`grok.provides` is required to disambiguate for what interface the
      adapter will be registered.

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

:class:`grok.Annotation`
========================

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

:class:`grok.JSON
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

   **Example:** ::

      import grok
      grok.define_permission('cave.enter')


   .. seealso::

      :func:`grok.require`, :class:`grok.Permission`, :class:`grok.Role`

   .. versionchanged:: 0.11
      replaced by :class:`grok.Permission`.

:class:`Role`
=============

Uncategorized
~~~~~~~~~~~~~

.. The weird classes we couldn' categorize yet

:class:`grok.Indexes`
=====================
