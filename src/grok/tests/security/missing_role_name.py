"""
A role has to have a name to be defined.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  GrokError: A role needs to have a dotted name for its id.
  Use grok.name to specify one.
"""

import grok
import zope.interface

class MissingName(grok.Role):
    pass
