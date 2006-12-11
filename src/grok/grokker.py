import grok
from grok import util, templatereg

class GrokkerRegistry(object):
    def __init__(self):
        self._grokkers = {}
        
    def registerGrokker(self, grokker):
        self._grokkers[grokker.component_class] = grokker

    def scan(self, module_info):
        components = {}
        for grokker in self._grokkers.values():
            components[grokker.component_class] = []
    
        module = module_info.getModule()
        for name in dir(module):
            obj = getattr(module, name)
            if name.startswith('__grok_'):
                continue
            if not util.defined_locally(obj, module_info.dotted_name):
                continue
            # XXX find way to get rid of this inner loop by doing hash table
            # lookup?
            for grokker in self._grokkers.values():
                if grokker.match(obj):
                    components[grokker.component_class].append((name, obj))
                    break

        return components

    def grok(self, module_info):
        scanned_results = self.scan(module_info)

        # XXX hardcoded in here which base classes are possible contexts
        # this should be made extensible
        possible_contexts = [obj for (name, obj) in
                             (scanned_results.get(grok.Model, []) +
                              scanned_results.get(grok.Container, []))]
        context = util.determine_module_context(module_info, possible_contexts)
        
        templates = templatereg.TemplateRegistry()

        # XXX because templates are instances and we need access to
        # registered module-level templates during class grokking,
        # we need to make sure we do PageTemplate grokking before any
        # other grokking. We need to revise this as we work out
        # extensible template grokking. Possibly we need to introduce
        # a priority for grokkers so we can sort them.
        page_templates = scanned_results.pop(grok.PageTemplate, None)
        if page_templates is not None:
            grokker = self._grokkers[grok.PageTemplate]
            for name, component in page_templates:
                grokker.register(context,
                                 name, component,
                                 module_info, templates)

        # XXX filesystem level templates need to be scanned for after
        # inline templates to produce the right errors
        templates.findFilesystem(module_info)

        # now grok the rest
        for component_class, components in scanned_results.items():
            grokker = self._grokkers[component_class]
            for name, component in components:
                grokker.register(context,
                                 name, component,
                                 module_info, templates)
    
        templates.registerUnassociated(context, module_info)


# deep meta mode here - we define grokkers for grok.ClassGrokker and
# grok.InstanceGrokker.

class MetaGrokker(grok.ClassGrokker):
    def register(self, context, name, factory, module_info, templates):
        grokkerRegistry.registerGrokker(factory())
    
class ClassGrokkerGrokker(MetaGrokker):
    component_class = grok.ClassGrokker

class InstanceGrokkerGrokker(MetaGrokker):
    component_class = grok.InstanceGrokker

# the global grokker registry
grokkerRegistry = GrokkerRegistry()

# register the meta grokkers manually as we can't grok those
grokkerRegistry.registerGrokker(ClassGrokkerGrokker())
grokkerRegistry.registerGrokker(InstanceGrokkerGrokker())
