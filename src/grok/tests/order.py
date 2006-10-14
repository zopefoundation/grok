import grok
from zope import interface

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)

class Cave(grok.Model):
    pass
