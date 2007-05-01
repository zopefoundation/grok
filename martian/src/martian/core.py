import types, inspect

from zope.interface import implements

from martian.interfaces import IMartian, IMultiMartian
from martian import util
from martian.components import (MartianBase, ClassMartian, InstanceMartian,
                                GlobalMartian)

def is_baseclass(name, component):
    return (type(component) is type and
            (name.endswith('Base') or
             util.class_annotation_nobase(component, 'grok.baseclass', False)))
        
class ModuleMartian(MartianBase):
    implements(IMultiMartian)

    def __init__(self, martian, global_martian=None):
        self._martian = martian
        self._global_martian = global_martian
        
    def grok(self, name, module, **kw):
        grokked_status = False
        if self._global_martian:
            grokked_status = self._global_martian.grok(name, module, **kw)
        martian = self._martian
    
        for name in dir(module):
            if name.startswith('__grok_'):
                continue
            obj = getattr(module, name)
            if not util.defined_locally(obj, module.__name__):
                continue
            if is_baseclass(name, obj):
                continue
            grokked = martian.grok(name, obj, **kw)
            if grokked:
                grokked_status = True

        return grokked_status
    
class MultiMartianBase(MartianBase):
    implements(IMultiMartian)

    def __init__(self):
        self._martians = {}
        
    def register(self, martian):
        key = martian.component_class
        martians = self._martians.setdefault(key, [])
        if martian not in martians:
            martians.append(martian)
    
    def grok(self, name, obj, **kw):
        used_martians = set()
        grokked_status = False
        for base in self.get_bases(obj):
            martians = self._martians.get(base)
            if martians is None:
                continue
            for martian in martians:
                if martian not in used_martians:
                    grokked = martian.grok(name, obj, **kw)
                    if grokked:
                        grokked_status = True
                    used_martians.add(martian)
        return grokked_status
    
class MultiInstanceMartian(MultiMartianBase):
    def get_bases(self, obj):
        return inspect.getmro(obj.__class__)

class MultiClassMartian(MultiMartianBase):
    def get_bases(self, obj):
        return inspect.getmro(obj)

class MultiGlobalMartian(MartianBase):
    implements(IMultiMartian)

    def __init__(self):
        self._martians = []

    def register(self, martian):
        self._martians.append(martian)

    def grok(self, name, module, **kw):
        grokked_status = False
        for martian in self._martians:
            status = martian.grok(name, module, **kw)
            if status:
                grokked_status = True
        return grokked_status

class MultiMartian(MartianBase):
    implements(IMultiMartian)
    
    def __init__(self):
        self._multi_instance_martian = MultiInstanceMartian()
        self._multi_class_martian = MultiClassMartian()

    def register(self, martian):
        if isinstance(martian, InstanceMartian):
            self._multi_instance_martian.register(martian)
        elif isinstance(martian, ClassMartian):
            self._multi_class_martian.register(martian)
        else:
            assert 0, "Unknown type of martian: %r" % martian

    def grok(self, name, obj, **kw):
        if type(obj) in (type, types.ClassType):
            return self._multi_class_martian.grok(name, obj, **kw)
        else:
            return self._multi_instance_martian.grok(name, obj, **kw)
