"""
Grok error because import model doesn't count as context:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grok.tests.adapter.importedmodel2.Painting'>,
  please use the 'context' directive.

"""
import grok
from grok.tests.adapter.adapter import Cave
from zope import interface

class IPainting(interface.Interface):
    pass

class Painting(grok.Adapter):
    """
    Grokking of this should fail because there's no model (only an
    imported one which doesn't count).
    """
    grok.implements(IPainting)
