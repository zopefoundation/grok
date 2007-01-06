"""
Subclasses of grok.GlobalUtility must implement exactly one interface:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.utility.implementsnone.Club'> must
  implement exactly one interface (use grok.implements to specify).
"""
import grok

class Club(grok.GlobalUtility):
    pass
