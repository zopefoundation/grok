import grok
from zope import interface
import persistent

class ISpecialPersistent(persistent.interfaces.IPersistent):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(ISpecialPersistent)

class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace)
