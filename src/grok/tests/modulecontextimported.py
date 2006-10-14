import grok
from grok.tests.adapter import Cave
from zope import interface

grok.context(Cave)

class IPainting(interface.Interface):
    pass

class Painting(grok.Adapter):
    grok.implements(IPainting)
