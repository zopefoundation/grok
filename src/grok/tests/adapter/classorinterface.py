"""
You can only use `grok.context` with interfaces or classes and not
with anything else:

  >>> function_context()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> string_context()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> module_context()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called with a class or an interface.

  >>> instance_context()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called with a class or an interface.

"""
import grok

def function_context():
    def a():
        pass

    class FunctionContext(object):
        grok.context(a)

def string_context():
    class StringContext(object):
        grok.context('string')

def module_context():
    class ModuleContext(object):
        grok.context(grok)

def instance_context():
    obj = object()
    class InstanceContext(object):
        grok.context(obj)
