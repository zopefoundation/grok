import grok
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grok.LocalUtility):
    grok.implements(IFireplace)

class Fireplace2(grok.LocalUtility):
    grok.implements(IFireplace)
    
class Cave(grok.Model, grok.Site):
    grok.local_utility(Fireplace, name='Foo')
    grok.local_utility(Fireplace2, name='Foo')
