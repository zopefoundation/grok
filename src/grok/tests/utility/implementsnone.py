"""
Subclasses of grok.GlobalUtility must implement exactly one interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: <class 'grok.tests.utility.implementsnone.Club'> must implement at least one interface (use grok.implements to specify).
"""  # noqa: E501
import grok


class Club(grok.GlobalUtility):
    pass
