"""
You can only use `grok.context` with interfaces or classes and not
with anything else:

  >>> function_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> string_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> module_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> instance_context()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be called with a class or an interface.

"""  # noqa: E501
import grok


def function_context():
    def a():
        pass

    class FunctionContext:
        grok.context(a)


def string_context():
    class StringContext:
        grok.context('string')


def module_context():
    class ModuleContext:
        grok.context(grok)


def instance_context():
    obj = object()

    class InstanceContext:
        grok.context(obj)
