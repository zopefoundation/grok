import grok
from grok import util, templatereg
from grok.error import GrokError

class GrokkerRegistry(object):
    def __init__(self):
        self.clear()

    def clear(self):
        self._grokkers = {}
        # register the meta grokkers manually as we can't grok those
        self.registerGrokker(ClassGrokkerGrokker())
        self.registerGrokker(InstanceGrokkerGrokker())
        self.registerGrokker(ModuleGrokkerGrokker())

    def registerGrokker(self, grokker):
        # we're using a dictionary to make sure each type of grokker
        # is registered only once (e.g. during meta-grok-time, and not again
        # during grok-time).
        key = grokker.__class__
        if key in self._grokkers:
            return
        self._grokkers[key] = grokker

    def _getGrokkersInOrder(self):
        # sort grokkers by priority
        grokkers = sorted(self._grokkers.values(),
                          key=lambda grokker: grokker.priority)
        # we want to handle high priority first
        grokkers.reverse()
        return grokkers

    def scan(self, module_info):
        components = {}
        for grokker in self._grokkers.values():
            if isinstance(grokker, grok.ModuleGrokker):
                continue
            components[grokker.component_class] = []

        grokkers = self._getGrokkersInOrder()
        module = module_info.getModule()
        for name in dir(module):
            if name.startswith('__grok_'):
                continue
            obj = getattr(module, name)
            if not util.defined_locally(obj, module_info.dotted_name):
                continue
            # XXX find way to get rid of this inner loop by doing hash table
            # lookup?
            for grokker in grokkers:
                if grokker.match(obj):
                    components[grokker.component_class].append((name, obj))
                    if not grokker.continue_scanning:
                        break

        return components

    def grok(self, module_info):
        scanned_results = self.scan(module_info)

        # XXX hardcoded in here which base classes are possible contexts
        # this should be made extensible
        possible_contexts = [obj for (name, obj) in
                             (scanned_results.get(grok.Model, []) +
                              scanned_results.get(grok.LocalUtility, []) +
                              scanned_results.get(grok.Container, []))]
        context = util.determine_module_context(module_info, possible_contexts)

        templates = templatereg.TemplateRegistry()

        # run through all grokkers registering found components in order
        for grokker in self._getGrokkersInOrder():
            # if we run into a ModuleGrokker, just do simple registration.
            # this allows us to hook up grokkers to the process that actually
            # do not respond to anything in the module but for instance
            # to the filesystem to find templates
            if isinstance(grokker, grok.ModuleGrokker):
                grokker.register(context, module_info, templates)
                continue

            components = scanned_results.get(grokker.component_class, [])

            for name, component in components:
                # this is a base class as it ends with Base, skip
                if type(component) is type:
                    if name.endswith('Base'):
                        continue
                    elif util.class_annotation_nobase(component,
                                                      'grok.baseclass', False):
                        continue
                grokker.register(context,
                                 name, component,
                                 module_info, templates)

        unassociated = list(templates.listUnassociated())
        if unassociated:
            raise GrokError("Found the following unassociated template(s) when "
                            "grokking %r: %s.  Define view classes inheriting "
                            "from grok.View to enable the template(s)."
                            % (module_info.dotted_name,
                               ', '.join(unassociated)), module_info)


# deep meta mode here - we define grokkers for grok.ClassGrokker,
# grok.InstanceGrokker, and grokker.ModuleGrokker.

class MetaGrokker(grok.ClassGrokker):
    def register(self, context, name, factory, module_info, templates):
        grokkerRegistry.registerGrokker(factory())

class ClassGrokkerGrokker(MetaGrokker):
    component_class = grok.ClassGrokker

class InstanceGrokkerGrokker(MetaGrokker):
    component_class = grok.InstanceGrokker

class ModuleGrokkerGrokker(MetaGrokker):
    component_class = grok.ModuleGrokker

# the global grokker registry
grokkerRegistry = GrokkerRegistry()

