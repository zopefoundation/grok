from zope.interface import Interface
import grok

class IMammoth(Interface):
    pass

class Mammoth(grok.GlobalUtility):
    grok.provides(IMammoth)
