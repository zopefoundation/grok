import grok
from grok.tests.adapter import Cave
from zope import interface

class IPainting(interface.Interface):
    pass

class Painting(grok.Adapter):
    """
    Grokking of this should fail because there's no model (only an
    imported one which doesn't count).
    """
    grok.implements(IPainting)
