import grok
from grok.tests.adapter import Cave

def func():
    """We don't allow calling `grok.context` from anything else than a
    module or a class"""
    grok.context(Cave)

class SomeClass(object):

    def meth(self):
        """We don't allow calling `grok.context` from anything else
        than a module or a class"""
        grok.context(Cave)
