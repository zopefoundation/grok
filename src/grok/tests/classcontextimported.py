import grok
from grok.tests.adapter import Cave
from zope import interface

class IPainting(interface.Interface):
    pass

class Painting(grok.Adapter):
    grok.implements(IPainting)
    grok.context(Cave)
