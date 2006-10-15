"""
Templates with ambiguous context cannot be grokked:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible contexts for
  <club template in grok.tests.view.ambiguouscontext>, please use grok.context.

"""

import grok

class Cave(grok.Model):
    pass

class Mammoth(grok.Model):
    pass

club = grok.PageTemplate("""\
<html><body><h1>GROK CLUB MAMMOTH!</h1></body></html>
""")
