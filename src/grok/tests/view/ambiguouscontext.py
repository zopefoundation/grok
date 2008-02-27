"""
Templates with ambiguous context cannot be grokked:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <class 'grok.tests.view.ambiguouscontext.Club'>, please use grok.context.

"""

import grok

class Cave(grok.Model):
    pass

class Mammoth(grok.Model):
    pass

class Club(grok.View):
    pass
