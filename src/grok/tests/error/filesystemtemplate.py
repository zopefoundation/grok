"""

This test checks for the right name in the error message if a filesystem-based
template can not find a context to be associated with:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
  GrokError: No module-level context for <nocontext template in ...grok/tests/error/filesystemtemplate/nocontext.pt>, please use grok.context.

"""
import grok
