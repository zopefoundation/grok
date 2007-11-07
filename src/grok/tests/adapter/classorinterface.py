"""
You can only use `grok.context` with interfaces or classes and not
with anything else:

  >>> function_context()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass classes or interfaces to grok.context.

  >>> stringcontext()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass classes or interfaces to grok.context.

  >>> module_context()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass classes or interfaces to grok.context.

  >>> instance_context()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass classes or interfaces to grok.context.

"""
import grok

def function_context():
    def a():
        pass

    class FunctionContext(object):
        grok.context(a)

def stringcontext():
    class StringContext(object):
        grok.context('string')

def module_context():
    class ModuleContext(object):
        grok.context(grok)

def instance_context():
    obj = object()
    class InstanceContext(object):
        grok.context(obj)
