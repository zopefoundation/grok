Grok changes
************

6.2 (unreleased)
================

- Nothing changed yet.


6.1 (2025-06-10)
================

* Drop support for Python 3.8.

* Require ``grokcore.view[security-publication]`` (with hyphen instead of
  underscore) as it seems to get name mangled somewhere along the way.

6.0 (2025-04-17)
================

* Make ``grokwiki`` example project work again.

* Re-enable ``zpassword`` in ``buildout.cfg``.

* Drop support for deprecated ``z3c.autoinclude``.

5.1 (2024-10-28)
================

* Add support for Python 3.13.

* Drop support for Python 3.7.


5.0 (2024-01-29)
================

Breaking changes
----------------

* Drop dependency on archived packages:

  * ``grokcore.xmlrpc``

  * ``grokcore.rest``

  * ``grokcore.json``

  * ``grokui.admin`` (only used in grokwiki example project)

Fixes
-----

* Fix GrokWiki example app.

* Fix installation documentation.

Changes
-------

* Split ``default.zcml`` off ``configure.zcml`` for easier exclude.

* Split ``dependencies.zcml`` off ``configure.zcml`` for easier reuse.


4.0 (2023-12-19)
================

* Add support for Python 3.11, 3.12.

* Update import paths for lifecycle events.

* Drop support for Python 2.7, 3.5, 3.6.


3.3 (2022-09-01)
================

* Add support for Python 3.9, 3.10.

* Fix deprecation warnings.


3.2 (2020-09-02)
================

* Fix DeprecationWarnings.

* Use zopefoundation/meta/config to harmonize package structure.

* Drop support for Python 3.4, add 3.7 + 3.8.

* Remove some backward compatibility imports.

3.1 (2018-05-09)
================

* Expose ``grok.ignore`` to allow not grokking something in a module.

3.0.1 (2018-01-17)
==================

* Replace the use of ``grok.implements()`` with the ``@grok.implementer()``
  directive throughout.

3.0.0 (2018-01-16)
==================

* Python 3 compatibility.

1.15 (2017-05-30)
=================

* Advertise the LazyAnnotation and LazyAnnotationProperty.

1.14.1 (2016-02-15)
===================

* Update tests.

1.14 (2015-06-11)
=================

Note: There are a couple of changes that breaks backward compatibility
with older versions.

* Advertise the ``install_on`` directive from grokcore.site.

* Replace ``ApplicationInitializedEvent`` with
  ``ApplicationAddedEvent`` from grokcore.site.

* Introduce a new event ``DatabaseCreatedEvent`` which is triggered
  only one time when the database is created. For existing application
  upgrade to this new version, an event will still be send at the time
  of the upgrade.

* Replace ``grok.util.create_application`` with the one from
  grokcore.site.util. It is now importable directly from grok.

1.13 (2015-06-04)
=================

* Advertise the ``ObjectEditedEvent`` from grokcore.content.

1.12 (2014-10-20)
=================

* Add ``grok.queryAnnotation()`` and ``grok.deleteAnnotation()`` from
  ``grokcore.annotation``.

1.11.3 (2013-04-03)
===================

* Fixed application_url() calls to use keyword arguments where the API
  defines keyword arguments.

1.11.2 (2013-04-03)
===================

* Fix brown paper bag release where not all resources were included. Again.

1.11.1 (2013-04-03)
===================

* Fix brown paper bag release where not all resources were included.

1.11 (2013-04-03)
=================

* Update ``grok.util.application_url()`` to work correctly with
  ``grokcore.view.util.url()``.

1.10.3 (2012-05-10)
===================

* Make sure the correct layout is retrieved for layout aware form components
  too.

1.10.2 (2012-05-10)
===================

* Import the grokcore.layout.layout directive into the grok namespace too.

1.10.1 (2012-05-02)
===================

* Update version requirements.

1.10 (2012-05-02)
=================

* Split off the Application component and the local_utility directive to
  grokcore.site. A backwards compatibility import for Application is left
  in place.

* Split off the catalog and indexing components from grok into
  grokcore.catalog.

* The permissions() directive, the Permission component and the Role
  component moved from grok to grokcore.security. The grok package imports
  these component, so they can still be accessed through the grok api.

1.9 (2011-09-06)
================

* Added imports for `querySubscriptions()`, `queryMultiSubscriptions()`,
  `queryOrderedSubscriptions()` and `queryOrderedMultiSubscriptions()` functions
  that complement the Subscriptions and MultiSubscriptions components.

1.8 (2011-07-14)
================

* Incorporate grokcore.chameleon and have it configured by default.

* Expose the Layout, Page, AddFormPage, EditFormPage, DisplayFormPage and
  FormPage components that are brought by grokcore.layout. The grok variants
  mixin application_url() and flash() functionality typically found in grok's
  viewish components.

* Expose the ExecptionPage, NotFoundPage and UnauthorizedPage component from
  grokcore.layout.

* Expose the ContentProvider component from grokcore.view

* Declare the name "index" as default view name for error views.

1.7 (2011-05-26)
================

* Directly depend on zope.app.wsgi and configure it too to have the useful
  IResult adapters for (temporary) files registered.

* Import grokcore.component.global_adapter too.

1.6 (2011-04-04)
================

* Fix tests that relied on older versions of zope.testbrowser.

* Added grok.index.Value component.

1.5 (2011-02-14)
================

* Added import for Subscription and MultiSubscription components.

1.4.3 (2011-02-08)
==================

* Fix tests now that error views no longer by default provide ISystemErrorView.

1.4.2 (2011-01-20)
==================

* Should've listed IApplication as part of the grok API too.

1.4.1 (2011-01-20)
==================

* Grok should still provide IApplication in the grok API, even now that it
  got moved to grokcore.site.interfaces.

1.4 (2011-01-20)
================

* Define error view baseclasses for IException, INotFound and IUnauthorized
  errors: grok.ExceptionView, grok.NotFoundView, grok.UnauthorizedView. Lifts
  the indirect dependency on zope.app.http and zope.app.exception.

* Moved the XMLRPC, REST component into separate packages
  grokcore.xmlrpc and grokcore.rest. Consequently the custom traverse
  components that Grok defined were moved to grokcore.traverser. Grok
  the-python-package acts more and more like an import-hub.

* To build the docs we now use `collective.recipe.sphinxbuilder`
  instead of our own, early hack (get rid of `grokdocs`
  subpackage). Buildout now generates ``grokdocs2html`` and
  ``grokdocs2pdf`` which should do what you think they do.

* The `IApplication` interface, and getApplication() moved to
  ``grokcore.site``.

1.3 (2010-11-03)
================

* The `IGrokSecurityView` interface has been to ``grokcore.view``.

* The `make_checker` util function has been moved to ``grokcore.view``.

* The base publisher has been moved to ``grokcore.view`` as an
  optional feature : security_publication.

* The JSON component and grokker are now moved to
  ``grokcore.json``. Grok now depends on this new grokore package.

* Update to latest martian and grokcore.component.

1.2.1 (2010-10-26)
==================

* Grok tutorial example projects updated.

* Documentation updates in preparation for the Grok Toolkit 1.2 release.

* Use zc.buildout-1.5.2.

1.2 (2010-10-13)
================

* No changes were necessary.

1.2a (2010-10-07)
=================

* Grok and the Grok Toolkit now use zc.buildout-1.5.1 that should simplify
  Grok's installation story significantly. It is now possible to use a system
  Python installation for installing Grok. This obsoletes the ``virtualenv``
  requirement.

* Grok and the Grok Toolkit will use the ZTK-1.0 release. Note though that
  several package versions are overridden to include bugfix releases.

* Various dependencies have been updated.

* Removed z3c.testsetup-specific test collector from grok.testing. You can
  still use z3c.testsetup with grok, but have to declare the dependency in your
  project's ``setup.py`` explicitly.

* The grok.View component now uses the grokcore.message package for its
  `flash` method.

* Grok test zcml now explicitly sets a defaultView name (to `index.html`).
  This has been added since we no longer depend on packages such as
  zope.app.zcmlfiles, that used to take care of that configuration step.

* Internationalization of title and description of roles are not lost anymore.

* `create_application` now raises a `KeyError`, in cases of key duplication,
  to match the ``zope.container`` behavior. Tests have been adapted accordingly.

* Added `KeyError` error handling to the existing `DuplicationError`, to fit
  the ``zope.container`` changes. Tests have been adapted accordingly.

1.1.1 (2010-05-30)
==================

* Make use of the groktoolkit 1.1.1 that includes several bugfix releases
  of Grok's dependencies such as:

  * zope.password, where the SSHAPasswordManager was fixed.

  * zope.publisher, that fixes the long standing XML-RPC "hanging" bug.

* Cleanups in the buildout parts.

* Remove zope.app.twisted.

1.1 (2010-05-18)
================

* Add zope.pluggablauth as a dependency.

1.1rc1 (2010-02-25)
===================

* Now using grokcore.content for the base content types : Model,
  Container and OrderedContainer.

* Lifted the dependency on zope.app.authentication and depend on
  zope.password instead.

* Lifted dependencies on deprecate packages zope.app.error and
  zope.app.securitypolicy and zope.app.session.

Beside these changes lot of work has been undertaken to remove as much
dependencies on "older" zope.app.* packages as possible from Grok itself
and from the dependencies of Grok. This work is not complete yet.

1.1a2 (2009-12-22)
==================

* Updated z3c.recipe.compattest's version and used it for a bin/compattest
  that tests grok and all its dependencies.

* Add grok.getApplication() that, similar to grok.getSite() retrieves
  the "nearest" enclosing grok.Application object.

* Use zope.container instead of zope.app.container.

* Use zope.catalog instead of zope.app.catalog.

* Use zope.intid instead of zope.app.intid.

* Use zope.keyreference instead of zope.app.keyreference.

1.1a1 (2009-11-17)
==================

* This release depends on grokcore.view 1.13a1.

* Add ZTK support (currently ZTK 1.0dev).

* Grokdocs now uses ZTK pinned versions.

* The ``grok.permissions()``, that is used in the ``grok.Role`` component now
  accepts references to ``grok.Permission`` class, not just permission ids.
  This behaviour is now symetrical to the ``grok.require()`` directive.

* Added an util function, ``create_application``, to create an
  application and trigger the correct events during the process.

* Grok now provides an application-centric event to complete the
  zope.lifecycle ones. This event, ``ApplicationInitializedEvent``, is
  destined to be trigged after the application has been added to a
  container. At this particular step, the application is considered
  safe for additional content to be created.

* Use grokcore.site and grokcore.annotation instead of builtins
  implementations.

* Update the reference to mention ``zope.View``.

* Update the reference to mention direct references to permissions in
  ``grok.require`` and ``grok.permissions`` in ``grok.Role``.

* Fix documentation bug where virtualenv wasn't explained correctly.

* Remove the ``grok.View`` permission declaration in ``etc/site.zcml.in``,
  should have gone in 1.0b2 already

1.0 (2009-10-07)
================

* Removed IReRaiseException adapter registration for IUnauthorized again in
  favor of using grokcore.startup's configurable``debug_application_factory``
  WSGI application factory function.

* Use newer versions of simplejson and pytz.

  See also https://bugs.launchpad.net/grok/+bug/432115

1.0b2 (2009-09-17)
==================

See: `upgrade_notes_1.0b2` for special notes on upgrading to this release.

* Revert back to an older version of ``grokui.admin`` that has not seen any
  changes related to the ``grok.View`` permission and the
  ``View``/``CodeView`` split and still has the introspector that is removed
  from newer versions.

* ``grokcore.view``, ``grokcore.viewlet`` and ``grokcore.formlib`` and
  Grok itself have been updated to undo the ``View``/``CodeView``
  split that we had temporarily introduced in the development versions
  after Grok 1.0a4.  This means the behavior of ``grok.View`` is
  unchanged from Grok 1.0a4. Nothing to see here!

* Changed the default permission to ``zope.View`` instead of
  ``zope.Public``. This means a modification needs to be made to your
  ``site.zcml`` if you're upgrading an existing Grok-based
  project. See the upgrade notes for more information.

  See also https://bugs.launchpad.net/grok/+bug/387332

* Bump used zope.app.wsgi version (now: 3.4.2) to support
  product-configs in zope.conf files with paster. Fix
  https://bugs.launchpad.net/grok/+bug/220440

* Default location for Data.fs and logfiles of grok's sample application is
  now ``var/filestorage/`` and ``var/log/`` instead of ``parts/data/``
  and ``parts/log/``.

* Bump used `z3c.testsetup` version (now: 0.4). Fix
  https://bugs.launchpad.net/grok/+bug/395125

* Bump used ZODB3 version (now: 3.8.3). Fix
  https://bugs.launchpad.net/grok/+bug/410703
  https://bugs.launchpad.net/grok/+bug/424335

* Added `zope.publisher.interfaces.IReRaiseException` adapter for
  IUnauthorized exceptions. Closes
  https://bugs.launchpad.net/grok/+bug/332061

* Removed `docutils` and `Pygment` from versions.cfg. Both are pinned
  in grokdocs subpackage. Closes
  https://bugs.launchpad.net/grok/+bug/340170

* Corrected Content-type; JSON views now report 'application/json'.

* updated zope.publisher dependency to 3.4.8 (fix paster.httpserver
  related bugs in XMLRPC, PUT)

* switched buildout to paster based template (like grokproject default)
  https://bugs.launchpad.net/grok/+bug/307197

* changed interpreter name from 'python' to 'grokpy'.

* Restructured the upgrade and change documentation so that they now
  get generated into separate files by Sphinx

1.0b1 (2009-09-14)
==================

* This release happened but never really was fully completed. See the
  release notes for 1.0b2 instead.

1.0a4 (2009-05-21)
==================

* Pin grokcore.view to 1.7.

* Import zope.app.container interfaces from their actual definition not from a
  re-import.

* JSON views now report a Content-type: text/json. See
  https://bugs.launchpad.net/bugs/362902


1.0a3 (2009-04-10)
==================

* Pin grokui.admin to 0.3.2

* Pin grokcore.view to 1.5.

* Pin grokcore.component to 1.6.


1.0a2 (2009-04-08)
==================

* Documentation and doc string updates.

* Pin grokui.admin to 0.3.

* Pin grokcore.view to 1.4.

* Synced versions.cfg with the latest KGS release available at:
  http://download.zope.org/zope3.4/3.4.0/versions.cfg

* Expose ``IBeforeTraverseEvent`` for import in the ``grok`` namespace.

1.0a1 (2009-01-08)
==================

See: `upgrade_notes_1.0a1` for special notes on upgrading to this release.

Feature changes
---------------

* Introduced ``grok.interfaces.IGrokSecurityView``, a marker interface
  which non-Grok views can use to state that they want to be handled
  like regular Grok views by the Grok publisher.

* Expose the ``DirectoryResource`` component from grokcore.view and the
  accompanying ``path`` directive.

* Similar to the layers and skins restructuring, the ``grok.RESTProtocol``
  baseclass has been removed in favour of a ``grok.restskin(name)`` directive
  that can be used on REST layer interfaces. Introduced the IRESTLayer base
  interfaces for defining REST layers.

* Besides our extensive existing documentation, we have also started
  to add a lot of docstrings to the Grok source code so it becomes
  easier to understand.

Bug fixes
---------

* Have GrokForm define an empty actions attribute by default, in order
  for "action-less" forms to work easily.

* Allow the grok.layer() directive on JSON components. Closes
  https://bugs.launchpad.net/grok/+bug/310558

* Close a bad security hole (also fixed in 0.14.1 and other
  releases). See
  http://grok.zope.org/blog/security-issue-in-grok-please-upgrade

Restructuring
-------------

* Viewlet-related base classes and helpers have been moved out to a
  ``grokcore.viewlet`` package which Grok now depends on.

0.14 (2008-09-29)
=================

See: `upgrade_notes_0.14` for special notes on upgrading to this release.

Feature changes
---------------

* Grok now officially supports Python 2.5 and still supports Python 2.4.

* Merged the versions from the zope 3.4c7 KGS (known good set):
  http://download.zope.org/zope3.4/versions-3.4.0c7.cfg
  So we are now using the latest Zope 3 releases for all Zope packages.

Restructuring
-------------

* The ``grok.admin`` subpackage has been factored out to a separate
  package ``grokui.admin``. To have the Grok admin UI available in
  your environment, add ``grokui.admin`` to the required packages in
  the ``setup.py`` of your package.

* Removed ``grok.Skin`` baseclass in favour of a ``grok.skin(name)``
  directive that can be used on layer interfaces.  Also removed the
  ``IGrokLayer`` interface in favour of exposing ``IBrowserRequest``
  from the grok package.

* Security-related directives and helpers have been moved out to a
  ``grokcore.security`` package.

* View-related base classes, directives and grokkers have been moved
  out to a ``grokcore.view`` package.

* Form-related base classes and helpers have been moved out to a
  ``grokcore.formlib`` package.

Bug fixes
---------

* Replace zope.deprecation.tests.warn with grok.testing.warn to:

    * Make the signature identical to warnings.warn

    * To check for \*.pyc and \*.pyo files.

  When zope.deprecation is fixed this warn() function can be removed again.
  Makes all the tests pass under Python-2.5.

0.13 (2008-06-23)
=================

See: `upgrade_notes_0.13` for special notes on upgrading to this release.

Restructuring
-------------

* The basic component base classes (``Adapter``, ``MultiAdapter``,
  ``GlobalUtility``), their grokkers, as well as many of the basic
  directives have been factored out to a reusable
  ``grokcore.component`` package.

* Ported directives to Martian's new directive implementation.  As a
  result, many helper functions that were available from ``grok.util``
  were removed.  The functionality is mostly available from the
  directives themselves now.

* Refactored class grokkers to make use of Martian's new declarative
  way for retrieving directive data from classes, and Martian's new
  declarative way to write grokkers. See `upgrade_notes_0.13`
  for more information.


Feature changes
---------------

* ``GrokTemplate`` sets up the namespaces for the template by calling
  ``default_namespace() ``on the view component the template is
  associated with. As a result, ``ViewletManagers`` and ``Viewlet``
  can now push in the ``viewletmanager`` and ``viewlet`` namespaces
  into the template.

* Updated tutorial section about grokproject to fit the latest changes.

* Added ``grok.traversable`` directive for easy traversal to attributes and
  methods.

* ``grok.require()`` can refer to subclasses of ``grok.Permission``
  directly, instead of their id. This, for one, avoids making typos in
  permission ids. Permission components *do* still need the
  grok.name() directive for defining the permission's id.

* Added an optional parameter ``data`` to the method ``url()`` that
  accepts a dictionary that is then converted to a query string. See

  http://grok.zope.org/documentation/how-to/generate-urls-with-the-url-function-in-views/view

* Added an ``OrderedContainer`` component.

* Introduced the new `sphinx`-based documentation engine. See
  grokdocs/README.txt for details.

* Merged the versions from the 3.4 KGS (known good set):
  http://download.zope.org/zope3.4/versions-3.4.0c1.cfg

  We are now using the latest Zope 3 releases for all Zope packages.
  See `upgrade_notes_0.13` for more information.

* Added support for easier test setup based on ``z3c.testsetup``. This
  is a more stable and more powerful implementation of
  ``grok.testing.register_all_tests()``. See

    http://grok.zope.org/documentation/how-to/tests-with-grok-testing

  for details.

* There is now a new ``IContext`` interface available. If you make
  your class implement that interface, it (and its subclasses) will be
  candidates for being a context in a module (for automatic context
  lookup if ``grok.context`` is not present). This relies on a feature
  introduced in ``grokcore.component`` 1.1.

* ``grok.Model`` implements ``grok.interfaces.IContext`` now (which is
  imported from ``grokcore.component``). ``grok.Container`` now
  implements ``grok.interfaces.IContainer``. Traversers and default
  views have been set up for these interfaces, so that new
  implementations that function as a model or container can be easily
  created. Just use ``grok.implements(IContainer)`` or
  ``grok.implements(IContext)``. This is useful for Grok extensions
  that want to implement new content classes.

Bug fixes
---------

* Fix https://bugs.launchpad.net/grok/+bug/226555: the ``url()`` method on
  ``ViewletManager`` and ``Viewlet`` has been removed now that there's easy
  access to the view component the viewlet(manager) is registered for.

* Fix https://bugs.launchpad.net/grok/+bug/231106: Use the
  viewletmanager.sort() method for sorting viewlets by using
  util.sort_components().

* grok.REST views now have a properly set ``__parent__`` attribute and
  will correctly allow acquisition from parent objects, as it's used
  by the security policy for acquiring local grants, for example.

* Fix https://bugs.launchpad.net/grok/+bug/229677:
  zope.app.securitypolicy egg missing. Now zope.app.securitypolicy
  3.4.6 is additionally required by Grok and fetched by buildout.

* Removed first testsetup hack from grok.testing.

* Version 2.1 of z3c.autoinclude contained code that caused Grok to
  fail to start on some platforms if the system-supplied Python was
  used (at least on some versions of Ubuntu and Debian). Now include
  version 2.2 of z3c.autoinclude which should fix this problem. This
  fix was also made on Grok 0.12 in its online versions list after
  release.

* Port fix of zope.formlib to correctly adapt the context to a FormField's
  interface, not the field.

0.12 (2008-04-22)
=================

See: `upgrade_notes_0.12` for special notes on upgrading to this release.

Feature changes
---------------

* The new release needs new version of grokproject, please do::

    $ easy_install -U grokproject

* Added testsetup classes in grok.testing to improve easy setup of
  unit* and functional tests.

* Add support for viewlets and viewlet managers, ``grok.Viewlet``
  and ``grok.ViewletManager``.

* Add a new directive, ``grok.order()``, which can be used to help
  sort components. At the time it is not used yet, but we intend to
  use it for the viewlets support. Note that this means Grok now
  requires Martian 0.9.3 or higher. See ``grok.interfaces`` for more
  documentation on this directive.

* Now depend on ``z3c.autoinclude``. This allows the use of the
  ``<includeDependencies package="."/>`` directive, which automatically loads
  up ZCML needed for the dependencies listed in your project's
  ``setup.py``. The new release of grokproject adds this line
  automatically. Upgrade ``grokproject`` to make use of this
  functionality in new projects::

    $ easy_install -U grokproject

* Classes that end with "-Base" are no longer implicitly considered base
  classes. These classes need to have the grok.baseclass() directive added to
  them explicitly.

  See `upgrade_notes_0.12` for more information.

Bug fixes
---------

* Do not register the publishTraverse and browserDefault methods of the
  JSON component as views.

* Methods with names that start with an '_' are not registered as views
  for XMLRPC, REST and JSON components.

* Use a configuration action for the registration of the static directory.

* Fix imports from zope.app.securitypolicy.

* Grok does not raise a GrokError anymore when it finds unassociated
  templates, but will issue a UserWarning.

* Fix https://bugs.launchpad.net/grok/+bug/161948: grok.testing.grok()
  now also loads the ZPT template factories so that unit tests that
  need to configure views with ZPT templates continue to work.

* Changed a few remaining references to ``grok.grok`` and
  ``grok.grok_component`` to their correct equivalents in
  ``grok.testing``.

* ``grok.testing.grok_component()`` could not be used in a pure
  doctest. This needed a bugfix in Martian (since 0.9.2). Add a test
  that demonstrates this problem.

* Fix https://bugs.launchpad.net/grok/+bug/162437: grok.Form and its
  subclasses did not implement IBrowserView.

* Fix https://bugs.launchpad.net/grok/+bug/185414: grok introspector
  was broken for zipped eggs.

* Fix https://bugs.launchpad.net/grok/+bug/125720: server control form
  had shutdown as default action, even when entering an admin message.

* Fix https://bugs.launchpad.net/grok/+bug/80403: Fix situation where
  a module name is identical to the package name. At least modules
  with templates can now have same name as their package.

* Multiple skins and REST protocols could be registered under the same
  name, but this is actually a conflict. Now give configuration
  conflict error when someone tries this.

* Overriding traversal behavior using the ``traverse()`` method or
  ``grok.Traverser`` failed in the face of (REST) ``PUT`` and
  ``DELETE``. XML-RPC also failed when custom traversal was in use.

* Fix https://bugs.launchpad.net/grok/+bug/187590 where config action
  discriminators for permission and role registrations were incorrect.

* Permission definitions received the wrong, too high, configure
  action priority (not to be confused with grokker priority). In some
  cases this caused permissions to be defined later than they were
  used. Use a low action priority instead for permissions.

Restructuring
-------------

* Refactor commonalities out of meta.py.

* zope.app.securitypolicy is no longer used. zope.securitypolicy provides
  all securitypolicy features used by Grok.

0.11 (2007-11-08)
=================

See: `upgrade_notes_0.11` for special notes on upgrading to this release.

Feature changes
---------------

* Integrated skins and layers: ``grok.layer``, ``grok.IGrokLayer``,
  ``grok.Skin``.

* Grok now supports hooking in new template languages without much work.
  See also doc/minitutorials/template-languages.txt. See Restructuring below
  for more techinical info.

* Accessing a template macro via context/@@the_view/the_template is now
  deprecated for the standard ZPT story of using
  context/@@the_view/macro/the_template.

* There is now a grok.direct() directive that can be used on GlobalUtilities
  to mark that the class provides the utility interface directly and need
  no instantiation.

* Removed ``grok.define_permission`` in favor of the
  ``grok.Permission`` component base class. You should now subclass
  this base class to define permissions. See also
  doc/minitutorials/permissions.txt

* Added the ``grok.Role`` component base class to define roles.

* The admin UI now displays and offers deletion of broken objects.

* Removed support for defining model schemas using an inner class with
  the special name ``fields``. This was abandoned in favor the usual
  Zope 3 way of defining schemas in interfaces and implementing them
  in our Grok models.

* Integrated REST support. See doc/minitutorials/rest.txt for usage
  information.

Bug fixes
---------

* Remove zc.recipe.egg, zc.recipe.filestorage, zc.recipe.testrunner,
  zc.zope3recipes from version requirements.

* The admin UI now shows interfaces in modules.

* ``handle...`` is not a special function name anymore.

* Views no longer need a custom ``AbsoluteURL`` view to determine
  their URL, since each instance now properly gets a ``__name__``
  attribute.

* buildout.cfg extends versions.cfg to pin down the versions of the
  dependency tree. See also http://grok.zope.org/releaseinfo/readme.html

Restructuring
-------------

* Grokkers now emit configuration actions, much like ZCML directive
  handlers do. If you defined custom grokkers,
  see `upgrade_notes_0.11` for more information.

* The new pluggable template language support includes some restructuring:

  * GrokPageTemplate is now split up into two. BaseTemplate, on which all
    templates need to be based, and GrokTemplate, which also provides a
    set of methods for easy integration of templating languages.

  * All objects based on GrokTemplate are now grokked, instead of having
    separate grokkers for each type of template.

  * The View is now completely template-language agnostic, which makes it
    easy to hook in new page template languages.

  * There are now new interfaces (ITemplate and ITemplateFileFactory)
    used when you implement support for a new templating language.

* Changed the way grok's functional tests are set up.  Instead of each
  test case doing its own test setup, it is now done once by the
  ftesting layer.  This avoids ordering problems when some ftests
  would influence the environment of other ftests that were run later
  in time.

0.10.2 (2007-10-24)
===================

Bug fixes
---------

* Remove zc.recipe.egg, zc.recipe.filestorage, zc.recipe.testrunner,
  zc.zope3recipes from version requirements.

* Require zope.app.error = 3.5.1

0.10.1 (2007-10-10)
===================

Bug fixes
---------

* buildout.cfg extends versions.cfg to pin down the versions of the
  dependency tree. This should avoid the situation where we release
  Grok, some dependency changes, and Grok breaks as a result. In
  conjunction with this we will also be releasing a new version of
  grokproject that will use this version infrastructure by default.

  For more information about this change, see:
  http://grok.zope.org/releaseinfo/readme.html

0.10 (2007-08-21)
=================

Feature changes
---------------

* Integrated admin user interface.

* Configuration using Martian (http://pypi.python.org/pypi/martian).

* Flash message infrastructure included.

* Adjust dependencies for Grok so that grokproject should work on
  Windows.

Bug fixes
---------

* A fix in Martian where multiple grok.Model or grok.Container classes
  could result in something being found as a context twice.

0.9 series (early 2007 until July 2007)
=======================================

Feature changes
---------------

Grok was released in "continuous release" mode from SVN during this period.

0.1 series (September 2006 until early 2007)
============================================

Feature changes
---------------

Grok was created in September 2006.
