import types

from zope.interface import implements

from martian.interfaces import INestedMartian
from martian import components, util

class ModuleMartian(components.MartianBase):
    implements(INestedMartian)

    def __init__(self):
        self._martians = {}
        
    def register(self, martian):
        # make sure martians are only registered once
        key = martian.__class__
        if key in self._martians:
            return
        self._martians[key] = martian

    def match(self, name, module):
        return isinstance(module, types.ModuleType)
    
    def grok(self, name, module, **kw):
        scanned_results = self._scan(module)
        # run through all martians registering found components in order
        for martian in self._get_ordered_martians():
            # if we run into a GlobalMartian, just do simple registration.
            # this allows us to hook up martians that actually
            # do not respond to anything in the module but for instance
            # go to the filesystem to find templates
            if isinstance(martian, components.GlobalMartian):
                martian.grok(name, module, **kw)
                continue

            found_components = scanned_results.get(martian.component_class, [])

            for name, component in found_components:
                # this is a base class as it ends with Base, skip
                if type(component) is type:
                    if name.endswith('Base'):
                        continue
                    elif util.class_annotation_nobase(component,
                                                      'grok.baseclass', False):
                        continue
                martian.grok(name, component, **kw)    

    def _scan(self, module):
        found_components = {}
        for martian in self._martians.values():
            if isinstance(martian, components.GlobalMartian):
                continue
            found_components[martian.component_class] = []

        martians = self._get_ordered_martians()

        for name in dir(module):
            if name.startswith('__grok_'):
                continue
            obj = getattr(module, name)
            if not util.defined_locally(obj, module.__name__):
                continue
            # XXX find way to get rid of this inner loop by doing hash table
            # lookup?
            for martian in martians:
                if martian.match(name, obj):
                    found_components[martian.component_class].append(
                        (name, obj))
                    if not martian.continue_scanning:
                        break

        return found_components

    def _get_ordered_martians(self):
        # sort martians by priority
        martians = sorted(self._martians.values(),
                          key=lambda martian: martian.priority)
        # we want to handle high priority first
        martians.reverse()
        return martians
