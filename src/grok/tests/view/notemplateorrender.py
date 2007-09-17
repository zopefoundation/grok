"""
Views either need an associated template or a ``render`` method:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: View <class 'grok.tests.view.notemplateorrender.CavePainting'>
  has no associated template or 'render' method.

"""

import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass
