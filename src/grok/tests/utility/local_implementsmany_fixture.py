import grok
from zope import interface

class IHome(interface.Interface):
    pass

class IFireplace(interface.Interface):
    pass

class Fireplace(object):
    interface.implements(IHome, IFireplace)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
