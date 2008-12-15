"""
We cannot register two rest protocols under the same name::

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  ConfigurationConflictError: Conflicting configuration actions
    For: ('restprotocol', 'foo')
"""

import grok

class Protocol1(grok.IRESTRequest):
    grok.restskin('foo')

class Protocol2(grok.IRESTRequest):
    grok.restskin('foo')
