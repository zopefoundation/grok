"""
It is an error for the 'static' directory to be a python package:

  >>> import grok
  >>> grok.testing.grok('grok.tests.static.staticispackage_fixture')
  Traceback (most recent call last):
    ...
  GrokError: The 'static' resource directory must not be a python package.
"""
