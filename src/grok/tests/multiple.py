import grok
from zope import interface

class Cave(grok.Model):
    pass

class Club(grok.Model):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
