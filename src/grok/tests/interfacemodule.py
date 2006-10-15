import grok
from zope import interface

class ICave(interface.Interface):
    pass

class Cave(grok.Model):
    grok.implements(ICave)

class Hole(grok.Model):
    grok.implements(ICave)

grok.context(ICave)

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
