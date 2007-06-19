import martian
from component import Alpha

class AlphaGrokker(martian.ClassGrokker):
    component_class = Alpha

    def grok(self, name, factory, context, module_info, templates):
        print "alpha"
        return True
