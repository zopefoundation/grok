"""
We define grokkers for the three base classes Alpha, Beta, and Gamma with different
priorities:
 
- AlphaGrokker with priority 0 (default)
- BetaGrokker with priority 1
- GammaGrokker with priority -1

    >>> grok.grok(__name__)

We grok a module that implements subclasses for Alpha, Beta, and Gamma and our
grokkers get executed in the order of priority (highest first)::

    >>> grok.grok('grok.tests.grokker.priority_fixture')
    beta
    alpha
    gamma

"""
import grok


class Alpha(object):
    pass


class Beta(object):
    pass

class Gamma(object):
    pass

class AlphaGrokker(grok.ClassGrokker):
    component_class = Alpha

    def grok(self, name, factory, context, module_info, templates):
        print "alpha"
        return True

class BetaGrokker(grok.ClassGrokker):
    component_class = Beta
    priority = 1

    def grok(self, name, factory, context, module_info, templates):
        print "beta"
        return True
    
class GammaGrokker(grok.ClassGrokker):
    component_class = Gamma
    priority = -1

    def grok(self, name, factory, context, module_info, templates):
        print "gamma"
        return True
