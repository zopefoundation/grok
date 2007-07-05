==========
Mars Macro
==========

Martian is a library that allows the embedding of configuration
information in Python code. Martian can then grok the system and
do the appropriate configuration registrations.

z3c packages bring significant clarity and a pattern for forms, view and
templates.

This package uses martian to configure z3c.macro based macros.

Example Code
------------

::

 class Navigation(mars.macro.MacroFactory):
     """Name defaults to factory.__name__, 'navigation'"""
     grok.template('templates/navigation.pt') # required
     grok.context(zope.interface.Interface) # required if no module context 

The following tal statement will look up the defined macro and insert its
template.::

 <div metal:use-macro="macro:naviagition" />

Directives
----------

Please see ``directive.txt``.

Tests
-----

See test directory.


