"""
You can't call grok.name on a module:

  >>> import grok.tests.view.nomodulename_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: The 'name' directive can only be used on class level.

"""
