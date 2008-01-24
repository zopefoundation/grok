
****
Core
****

The :mod:`grok` module defines a few functions to interact with grok itself.


:func:`grok.grok` -- Grok a package or module
=============================================


.. function:: grok(dotted_name)

   Grokking a package or module activates the contained components (like models,
   views, adapters, templates, etc.) and registers them with Zope 3's component
   architecture.

   The `dotted_name` must specify either a Python module or package that is
   available from the current PYTHONPATH.

   Grokking a module:

#. Scan the module for known components: models, adapters, utilities, views,
      traversers, templates and subscribers.

#. Check whether a directory with file system templates exists
      (:file:`<modulename>_templates`).  If it exists, load the file system templates
      into the template registry for this module.

#. Determine the module context.

#. Register all components with the Zope 3 component architecture.

#. Initialize schemata for registered models

   Grokking a package:

#. Grok the package as a module.

#. Check for a static resource directory (:file:`static`) and register it if it
      exists.

#. Recursively grok all sub-modules and sub-packages.

