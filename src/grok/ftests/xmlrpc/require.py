"""
  >>> from zope.app.testing.xmlrpc import ServerProxy
  >>> server = ServerProxy("http://localhost/")
  >>> mgr_server = ServerProxy("http://mgr:mgrpw@localhost/")

We can access a public method just fine, but a protected method will
raise Unauthorized:

  >>> print server.stomp()
  Manfred stomped.

  >>> print server.dance()
  Traceback (most recent call last):
  ProtocolError: <ProtocolError for localhost/: 401 401 Unauthorized>

With manager privileges, the protected method is accessible, however:

  >>> print mgr_server.dance()
  Manfred doesn't like to dance.

The same applies when a default permission is defined for all XML-RPC
methods in a class:

  >>> print server.hunt()
  Traceback (most recent call last):
  ProtocolError: <ProtocolError for localhost/: 401 401 Unauthorized>

  >>> print mgr_server.hunt()
  ME GROK LIKE MAMMOTH!

  >>> print server.eat()
  MMM, MANFRED TASTE GOOD!

  >>> print server.rest()
  ME GROK TIRED!
"""
import grok
import zope.interface

class MammothRPC(grok.XMLRPC):
    grok.context(zope.interface.Interface)

    def stomp(self):
        return 'Manfred stomped.'

    @grok.require('zope.ManageContent')
    def dance(self):
        return 'Manfred doesn\'t like to dance.'

class CavemanRPC(grok.XMLRPC):
    grok.context(zope.interface.Interface)
    grok.require('zope.ManageContent')

    def hunt(self):
        return 'ME GROK LIKE MAMMOTH!'

    @grok.require('zope.View')
    def eat(self):
        return 'MMM, MANFRED TASTE GOOD!'

    @grok.require(grok.Public)
    def rest(self):
        return 'ME GROK TIRED!'
