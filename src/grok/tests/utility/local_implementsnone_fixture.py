import grok
from zope import interface

class Fireplace(object):
    pass

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
