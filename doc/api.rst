API reference
=============

.. py:module:: grok

Content model and container components
--------------------------------------

.. autoclass:: grok.Application
.. autoclass:: grok.Container
.. autoclass:: grok.Model
.. autoclass:: grok.OrderedContainer
.. autoclass:: grok.Site
.. autofunction:: grok.getApplication
.. autofunction:: grok.getSite

View components
---------------

.. autoclass:: grok.DirectoryResource
.. autoclass:: grok.IBrowserRequest
.. autoclass:: grok.IDefaultBrowserLayer
.. autoclass:: grok.IRESTLayer
.. autoclass:: grok.IRESTSkinType
.. autoclass:: grok.JSON
.. autoclass:: grok.layer
.. autoclass:: grok.PageTemplate
.. autoclass:: grok.PageTemplateFile
.. autoclass:: grok.path
.. autoclass:: grok.REST
.. autoclass:: grok.restskin
.. autoclass:: grok.skin
.. autoclass:: grok.template
.. autoclass:: grok.view
.. autoclass:: grok.View
.. autoclass:: grok.Viewlet
.. autoclass:: grok.viewletmanager
.. autoclass:: grok.ViewletManager
.. autoclass:: grok.XMLRPC
.. autofunction:: grok.url

Forms
-----

.. autoclass:: grok.action
.. autoclass:: grok.AddForm
.. autoclass:: grok.DisplayForm
.. autoclass:: grok.EditForm
.. autoclass:: grok.Form
.. autofunction:: grok.AutoFields
.. autofunction:: grok.Fields

Utilities, Adapters, Subscriptions
----------------------------------

.. autoclass:: grok.adapter
.. autoclass:: grok.Adapter
.. autoclass:: grok.Annotation
.. autoclass:: grok.global_utility
.. autoclass:: grok.GlobalUtility
.. autoclass:: grok.implementer
.. autoclass:: grok.local_utility
.. autoclass:: grok.LocalUtility
.. autoclass:: grok.MultiAdapter
.. autoclass:: grok.MultiSubscription
.. autoclass:: grok.Subscription
.. autofunction:: grok.adapts
.. autofunction:: grok.implements

Security
--------

.. autoclass:: grok.Permission
.. autoclass:: grok.permissions
.. autoclass:: grok.Public
.. autoclass:: grok.require
.. autoclass:: grok.Role

Traversal
---------

.. autoclass:: grok.Traverser
.. autoclass:: grok.traversable

Indexes
-------

.. autoclass:: grok.Indexes
.. autoclass:: grok.index.Field
.. autoclass:: grok.index.Set
.. autoclass:: grok.index.Text

Events and event handling
-------------------------

.. autoclass:: grok.ApplicationInitializedEvent
.. autoclass:: grok.ContainerModifiedEvent
.. autoclass:: grok.IBeforeTraverseEvent
.. autoclass:: grok.IContainerModifiedEvent
.. autoclass:: grok.IObjectAddedEvent
.. autoclass:: grok.IObjectCopiedEvent
.. autoclass:: grok.IObjectCreatedEvent
.. autoclass:: grok.IObjectModifiedEvent
.. autoclass:: grok.IObjectMovedEvent
.. autoclass:: grok.IObjectRemovedEvent
.. autoclass:: grok.ObjectAddedEvent
.. autoclass:: grok.ObjectCopiedEvent
.. autoclass:: grok.ObjectCreatedEvent
.. autoclass:: grok.ObjectModifiedEvent
.. autoclass:: grok.ObjectMovedEvent
.. autoclass:: grok.ObjectRemovedEvent
.. autoclass:: grok.viewletmanager
.. autofunction:: grok.notify
.. autofunction:: grok.subscribe

Directives
----------

.. autoclass:: grok.baseclass
.. autoclass:: grok.context
.. autoclass:: grok.description
.. autoclass:: grok.direct
.. autoclass:: grok.global_utility
.. autoclass:: grok.layer
.. autoclass:: grok.name
.. autoclass:: grok.permissions
.. autoclass:: grok.provides
.. autoclass:: grok.require
.. autoclass:: grok.restskin
.. autoclass:: grok.site
.. autoclass:: grok.skin
.. autoclass:: grok.template
.. autoclass:: grok.title
.. autoclass:: grok.view
.. autoclass:: grok.viewletmanager

Grokkers
--------

.. autoclass:: grok.ClassGrokker
.. autoclass:: grok.GlobalGrokker
.. autoclass:: grok.GrokError
.. autoclass:: grok.GrokImportError
.. autoclass:: grok.InstanceGrokker
.. autofunction:: grok.testing.grok
.. autofunction:: grok.testing.grok_component
.. autofunction:: grok.testing.warn
