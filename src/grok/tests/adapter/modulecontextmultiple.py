"""
You can't call grok.context multiple times on module level:

  >>> import grok.tests.adapter.modulecontextmultiple_fixture
  Traceback (most recent call last):
    ...
  GrokError: grok.context can only be called once per class or module.

"""
