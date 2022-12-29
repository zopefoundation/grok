"""
A permission has to be defined first (using grok.Permission for example)
before it can be used in @grok.require().

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  zope.configuration.config.ConfigurationExecutionError:
      martian.error.GrokError: Undefined permission 'doesnt.exist' in <class 'grok.tests.xmlrpc.missing_permission2.MissingPermission'>. Use grok.Permission first.
"""  # noqa: E501

import zope.interface

import grok


class MissingPermission(grok.XMLRPC):
    grok.context(zope.interface.Interface)

    @grok.require('doesnt.exist')
    def foo(self):
        pass
