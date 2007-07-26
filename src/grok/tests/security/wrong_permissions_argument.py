"""
The grok.define_role needs a sequence of permission ids::

  >>> grok.grok('grok.tests.security.wrong_permissions_argument_fixture')
  Traceback (most recent call last):
  GrokImportError: You need to pass a list or tuple of permission ids to
  the permissions argument of grok.define_role.


"""

import grok
