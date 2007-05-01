import types

from zope.interface import implements

from martian.interfaces import IMartian, IMultiMartian
from martian import components, util

def is_baseclass(name, component):
    return (type(component) is type and
            (name.endswith('Base') or
             util.class_annotation_nobase(component, 'grok.baseclass', False)))
        
class ModuleMartian(components.MartianBase):
    implements(IMartian)

    def __init__(self, martian):
        self._martian = martian

    def match(self, name, module):
        return isinstance(module, types.ModuleType)
    
    def grok(self, name, module, **kw):
        martian = self._martian
        
        if isinstance(martian, components.GlobalMartian):
            martian.grok(name, module, **kw)
            return

        for name in dir(module):
            if name.startswith('__grok_'):
                continue
            obj = getattr(module, name)
            if not util.defined_locally(obj, module.__name__):
                continue
            if is_baseclass(name, obj):
                continue
            if not martian.match(name, obj):
                continue
            martian.grok(name, obj, **kw)

class MultiMartianBase(components.MartianBase):
    implements(IMultiMartian)

    def __init__(self):
        self._martians = {}
        
    def register(self, martian):
        key = martian.component_class
        martians = self._martians.setdefault(key, [])
        if martian not in martians:
            martians.append(martian)
    
    def match(self, name, obj):
        for martians in self._martians.values():
            for martian in martians:
                if martian.match(name, obj):
                    return True
        return False

    def grok(self, name, obj, **kw):
        used_martians = set()
        for base in self.get_bases(obj):
            martians = self._martians.get(base)
            if martians is None:
                continue
            for martian in martians:
                if martian not in used_martians:
                    martian.grok(name, obj, **kw)
                    used_martians.add(martian)
        
class MultiInstanceMartian(MultiMartianBase):
    def get_bases(self, obj):
        # XXX how to work with old-style classes?
        return obj.__class__.__mro__

class MultiClassMartian(MultiMartianBase):
    def get_bases(self, obj):
        # XXX how to work with old-style classes?
        return obj.__mro__

class MultiMartian(components.MartianBase):
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
        if type(obj) is type:
            self._multi_class_martian.grok(name, obj, **kw)
        else:
            self._multi_instance_martian.grok(name, obj, **kw)
