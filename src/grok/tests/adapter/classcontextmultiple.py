"""
You can't call grok.context multiple times on class level:

  >>> import grok.tests.adapter.classcontextmultiple_fixture
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be called once per class or module.
"""  # noqa: E501
