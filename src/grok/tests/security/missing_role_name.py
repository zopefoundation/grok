"""
A role has to have a name to be defined.

  >>> grok.grok(__name__)
  Traceback (most recent call last):
  ...
  AttributeError: 'MissingName' object has no attribute 'id'
"""

import grok
import zope.interface

class MissingName(grok.Role):
    pass
