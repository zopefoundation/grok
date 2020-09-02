"""
The permissions() directive only accepts permission ids or permission classes:

  >>> import grok
  >>> grok.testing.grok('grok.tests.security.not_a_permission_class_fixture')
  Traceback (most recent call last):
  ...
  martian.error.GrokImportError: You can only pass unicode values, ASCII values, or subclasses of grok.Permission to the 'permissions' directive.

"""  # noqa: E501
