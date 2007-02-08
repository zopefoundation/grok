import grok
from component import Alpha

class AlphaGrokker(grok.ClassGrokker):
    component_class = Alpha

    def register(self, context, name, factory, module_info, templates):
        print "alpha"
