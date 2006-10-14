import grok
from zope import interface

class ZCave(grok.Model):
    """we call this `ZCave` because we want to test that we do not
    depend on alphabetical order"""

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
