"""
You can't call grok.context multiple times on class level:

  >>> import grok.tests.adapter.classcontextmultiple_fixture
  Traceback (most recent call last):
    ...
  GrokError: grok.context can only be called once per class or module.

"""

