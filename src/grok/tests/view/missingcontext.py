"""
Templates without a context cannot be grokked:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <club template in grok.tests.view.missingcontext>, please use grok.context.

"""

import grok

club = grok.PageTemplate("""\
<html><body><h1>GROK CLUB MAMMOTH!</h1></body></html>
""")
