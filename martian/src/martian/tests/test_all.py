import unittest
from zope.testing import doctest
import new

class FakeModule(object):
    pass

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
        setattr(module, name, obj)
        glob[name] = obj
    # provide correct globals for functions
    for name in dir(module):
        if name.startswith('__'):
            continue
        obj = getattr(module, name)
        try:
            code = obj.func_code
        except AttributeError:
            continue
        new_func = new.function(code, glob, name)
        new_func.__module__ = module.__name__
        setattr(module, name, new_func)
        glob[name] = new_func
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
