"""
A role has to have a name to be defined.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  martian.error.GrokError: A role needs to have a dotted name for its id.  Use grok.name to specify one.
"""  # noqa: E501

import grok


class MissingName(grok.Role):
    pass
