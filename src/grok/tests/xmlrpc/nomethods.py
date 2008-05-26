"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.xmlrpc.nomethods.RemoteCaveman'> does not
  define any public methods. Please add methods to this class to enable
  its registration.

"""
import grok

class Caveman(grok.Model):
    pass

class RemoteCaveman(grok.XMLRPC):
    pass
