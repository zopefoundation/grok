
**********
Exceptions
**********

grok tries to inform you about errors early and with as much guidance
as possible. grok can detect some errors already while importing a
module, which will lead to the :class:`GrokImportError`.  Other errors
require more context and can only be detected while executing the
:func:`grok` function.


:class:`grok.GrokImportError` -- errors while importing a module
================================================================

This exception is raised if a grok-specific problem was found while
importing a module of your application. :class:`GrokImportError` means
there was a problem in how you are using a part of grok. The error
message tries to be as informative as possible tell you why something
went wrong and how you can fix it.

:class:`GrokImportError` is a subclass of Python's
:class:`ImportError`.

Examples of situations in which a GrokImportError occurs:

  * Using a directive in the wrong context (e.g. grok.templatedir on
    class-level instead of module-level.)

  * Using a decorator with wrong arguments (e.g. grok.subscribe
    without any argument)

  * ...


:class:`grok.GrokError` -- errors while grokking a module
=========================================================

This exception is raised if an error occurs while grokking a module.

Typically a :class:`GrokError` will be raised if one of your modules
uses a feature of grok that requires some sort of unambigous context
to establish a reasonable default.

For example, the :class:`grok.View` requires exactly one model to be
defined locally in the module to assume a default module to be
associated with. Having no model defined, or more than one model, will
lead to an error because the context is either underspecified or
ambigous.

The error message of a :class:`GrokError` will include the reason for
the error, the place in your code that triggered the error, and a
hint, to help you fix the error.


.. class:: GrokError(Exception)

   .. attribute:: GrokError.component

      The component that was grokked and triggered the error.

