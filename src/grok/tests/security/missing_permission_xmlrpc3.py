"""
A permission has to be defined first (using grok.Permission for example)
before it can be used in grok.require() in an XMLRPC class. This is even the
case for a default permission that is never used.

  >>> grok.grok(__name__)
  Traceback (most recent call last):
   ...
  GrokError: Undefined permission 'doesnt.exist' in <class
  'grok.tests.security.missing_permission_xmlrpc3.MissingPermission'>. Use
  grok.Permission first.

"""

import grok
import zope.interface

class Foo(grok.Permission):
    grok.name('foo')

class MissingPermission(grok.XMLRPC):
    grok.context(zope.interface.Interface)
    grok.require('doesnt.exist')

    @grok.require('foo')
    def foo(self):
        pass
