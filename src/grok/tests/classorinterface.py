"""
All of the below examples should fail
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
