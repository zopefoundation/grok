"""

Context-determination follows the same rules as for adapters. We just check
whether it's hooked up at all:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grok.tests.json.nocontext.TestJSON'>, please use grok.context.

"""
import grok

class TestJSON(grok.JSON):
    pass
