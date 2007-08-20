"""
A role has to have a name to be defined.

  >>> grok.grok(__name__)
  Traceback (most recent call last):
  ...
  GrokError: A permission needs to have a dotted name for its id.
  Use grok.name to specify one.
"""

import grok
import zope.interface

class MissingName(grok.Permission):
    pass
