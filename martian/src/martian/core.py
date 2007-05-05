import types, inspect

from zope.interface import implements

from martian.interfaces import IGrokker, IMultiGrokker
from martian import util
from martian.components import (GrokkerBase, ClassGrokker, InstanceGrokker,
                                GlobalGrokker)

class ModuleGrokker(GrokkerBase):
    implements(IMultiGrokker)

    def __init__(self, grokker=None):
        if grokker is None:
            grokker = MultiGrokker()
        self._grokker = grokker

    def register(self, grokker):
        self._grokker.register(grokker)
        
    def grok(self, name, module, **kw):
        grokked_status = False
        grokker = self._grokker

        # trigger any global grokkers
        grokked = grokker.grok(name, module, **kw)
        if grokked:
            grokked_status = True

        # try to grok everything in module
        for name in dir(module):
            if name.startswith('__grok_'):
                continue
            obj = getattr(module, name)
            if not util.defined_locally(obj, module.__name__):
                continue
            if util.is_baseclass(name, obj):
                continue
            grokked = grokker.grok(name, obj, **kw)
            if grokked:
                grokked_status = True

        return grokked_status
    
class MultiGrokkerBase(GrokkerBase):
    implements(IMultiGrokker)

    def __init__(self):
        self._grokkers = {}
        
    def register(self, grokker):
        key = grokker.component_class
        grokkers = self._grokkers.setdefault(key, [])
        if grokker not in grokkers:
            grokkers.append(grokker)
    
    def grok(self, name, obj, **kw):
        used_grokkers = set()
        grokked_status = False
        for base in self.get_bases(obj):
            grokkers = self._grokkers.get(base)
            if grokkers is None:
                continue
            for grokker in grokkers:
                if grokker not in used_grokkers:
                    grokked = grokker.grok(name, obj, **kw)
                    if grokked:
                        grokked_status = True
                    used_grokkers.add(grokker)
        return grokked_status
    
class MultiInstanceGrokker(MultiGrokkerBase):
    def get_bases(self, obj):
        return inspect.getmro(obj.__class__)

class MultiClassGrokker(MultiGrokkerBase):
    def get_bases(self, obj):
        if type(obj) is types.ModuleType:
            return []
        return inspect.getmro(obj)

class MultiGlobalGrokker(GrokkerBase):
    implements(IMultiGrokker)

    def __init__(self):
        self._grokkers = []

    def register(self, grokker):
        self._grokkers.append(grokker)

    def grok(self, name, module, **kw):
        grokked_status = False
        for grokker in self._grokkers:
            status = grokker.grok(name, module, **kw)
            if status:
                grokked_status = True
        return grokked_status

class MultiGrokker(GrokkerBase):
    implements(IMultiGrokker)
    
    def __init__(self):
        self._multi_instance_grokker = MultiInstanceGrokker()
        self._multi_class_grokker = MultiClassGrokker()
        self._multi_global_grokker = MultiGlobalGrokker()
        
    def register(self, grokker):
        if isinstance(grokker, InstanceGrokker):
            self._multi_instance_grokker.register(grokker)
        elif isinstance(grokker, ClassGrokker):
            self._multi_class_grokker.register(grokker)
        elif isinstance(grokker, GlobalGrokker):
            self._multi_global_grokker.register(grokker)
        else:
            assert 0, "Unknown type of grokker: %r" % grokker

    def grok(self, name, obj, **kw):
        obj_type = type(obj)
        if obj_type in (type, types.ClassType):
            return self._multi_class_grokker.grok(name, obj, **kw)
        elif obj_type is types.ModuleType:
            return self._multi_global_grokker.grok(name, obj, **kw)
        else:
            return self._multi_instance_grokker.grok(name, obj, **kw)

# deep meta mode here - we define grokkers that can pick up the
# three kinds of grokker: ClassGrokker, InstanceGrokker and ModuleGrokker
class MetaGrokker(ClassGrokker):
    def grok(self, name, obj, **kw):
        the_grokker.register(obj())

class ClassMetaGrokker(MetaGrokker):
    component_class = ClassGrokker

class InstanceMetaGrokker(MetaGrokker):
    component_class = InstanceGrokker

class GlobalMetaGrokker(MetaGrokker):
    component_class = GlobalGrokker
    
# the global single grokker to bootstrap everything
the_grokker = MultiGrokker()
# bootstrap the meta-grokkers
the_grokker.register(ClassMetaGrokker())
the_grokker.register(InstanceMetaGrokker())
the_grokker.register(GlobalMetaGrokker())
