import martian
from component import Alpha

class AlphaGrokker(martian.ClassGrokker):
    component_class = Alpha

    def grok(self, name, factory, module_info, **kw):
        print "alpha"
        return True
