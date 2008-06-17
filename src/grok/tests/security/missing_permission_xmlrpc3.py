"""
A permission has to be defined first (using grok.Permission for
example) before it can be used in grok.require() in an XMLRPC
class. However, this is *not* the the case for a default permission
that is never used.

  >>> grok.testing.grok(__name__)

"""

import grok
import zope.interface

class Foo(grok.Permission):
    grok.name('foo')

class MissingPermission(grok.XMLRPC):
    grok.context(zope.interface.Interface)
    grok.require('doesnt.exist')

    @grok.require(Foo)
    def foo(self):
        pass
