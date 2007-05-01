import unittest
from zope.testing import doctest
import new, types

class FakeModule(object):
    pass

def class_annotation_nobase(obj, name, default):
    """This will only look in the given class obj for the annotation.

    It will not look in the inheritance chain.
    """
    return obj.__dict__.get('__%s__' % name.replace('.', '_'), default)

def fake_import(fake_module):
    module = new.module(fake_module.__name__)
    glob = {}
    for name in dir(fake_module):
        if name.startswith('__'):
            continue
        obj = getattr(fake_module, name)
        glob[name] = obj
        try:
            obj = obj.im_func
        except AttributeError:
            pass
        __module__ = None
        try:
            __module__ == obj.__dict__.get('__module__')
        except AttributeError:
            try:
                __module__ = obj.__module__
            except AttributeError:
                pass
        if __module__ is None or __module__ == '__builtin__':
            try:
                obj.__module__ = module.__name__
            except AttributeError:
                pass
        setattr(module, name, obj)

    # provide correct globals for functions
    for name in dir(module):
        if name.startswith('__'):
            continue
        obj = getattr(module, name)
        try:
            code = obj.func_code
            new_func = new.function(code, glob, name)
            new_func.__module__ = module.__name__
            setattr(module, name, new_func)
            glob[name] = new_func
        except AttributeError:
            pass
    return module

optionflags = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS

globs = dict(FakeModule=FakeModule, fake_import=fake_import)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        doctest.DocFileSuite('../README.txt',
                             globs=globs,
                             optionflags=optionflags),
        doctest.DocFileSuite('../scan.txt',
                             optionflags=optionflags),
        ])
    return suite
