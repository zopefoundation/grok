"""
Views without a context cannot be grokked:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grok.tests.view.missingcontext.Club'>, please use grok.context.

"""

import grok

class Club(grok.View):
    pass
