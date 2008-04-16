"""
Make sure we get an error for a missing permission even if that permission
isn't actually used (as there are more specific permissions)::

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  ConfigurationExecutionError: martian.error.GrokError: Undefined permission
  'doesnt.exist' in ...

"""

import grok
import zope.interface

class Permission(grok.Permission):
    grok.name('json.exists')

class MissingPermission(grok.JSON):
    grok.context(zope.interface.Interface)

    grok.require('doesnt.exist')
    
    @grok.require('json.exists')
    def foo(self):
        pass

