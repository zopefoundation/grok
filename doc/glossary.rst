=================
Grok Glossary
=================

* **adapter** - 
  An Adapter takes an object providing an existing interface and extends it to 
  provide a new interface.

* **(Grok) application** - 
  Applications are top-level objects. They are typically used to hold global 
  configuration and behaviour for an application instance, as well as holding 
  data objects such as grok.Container and grok.Model object instances.
  
* **buildout** -
  ...

* **buildout egg** -
  ...

* **(Grok) container** - 
  Objects in a container are manipulated using the same syntax as you would with
  a standard Python Dictionary object. The container implements the 
  zope.app.container.interfaces.IContainer interface using a BTree, providing 
  reasonable performance for large collections of objects.

* **(Grok) directive** - 
  The grok module defines a set of directives that allow you to configure and 
  register your components.

* **directory resource** - 
  ...

* **egg** - 
  ...

* **global utility** - 
  A global utility is an object which provides an interface, and can be 
  looked-up by that interface and optionally the component name. The attributes 
  provided by a global utility are not persistent.

* **grokproject** - 
  A command line tool for creating a Grok project using buildout.

* **layer** -
  A layer for the view.

* **local utility** -
  A local utility is an object which provides an interface, and can be looked-up
  by that interface and optionally the component name. The attributes provided 
  by a local utility are transparently stored in the database (ZODB). This means
  that configuration changes to a local utility lasts between server restarts.

* **martian** - 
  ...

* **megrok** - 
  ...

* **(Grok) model** - 
  Model objects provide persistence and containment. Model in Grok refers to an 
  applications data model - that is data which is persistently saved to disk, by
  default in the Zope Object Dataabse (ZODB).

* **Python Cheeseshop** -
  ...

* **(Grok) site** - 
  Contains a Site Manager. Site Managers act as containers for registerable 
  components.

* **skin** - 
  A named layer.

* **(Grok) view** - 
  Views handle interactions between the user and the model. 

* **viewlet** - 
  Viewlets are a flexible way to compound HTML snippets.

* **viewlet manager** - 
  A ViewletManager is a component that provides access to a set of content 
  providers (Viewlets). 

* **zc.buildout** - 
  see buildout

* **zc.resourcelibrary** - 
  ...

* **ZCML** - 
  Zope Configuration Markup Language

* **ZODB** - 
  Zope Object Database

* **ZPT** -
  Zope Page Template


