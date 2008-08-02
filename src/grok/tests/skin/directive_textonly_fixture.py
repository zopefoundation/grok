import grok
from zope.interface import Interface

some_obj = object()

class BogusSkin(Interface):
    grok.skin(some_obj)
