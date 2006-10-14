import grok
from zope import interface

class Cave(grok.Model):
    pass

class Club(grok.Model):
    pass

grok.context(Cave)

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
