import grok
from zope import interface

class IIsInterface(interface.Interface):
    grok.skin('skin name')
