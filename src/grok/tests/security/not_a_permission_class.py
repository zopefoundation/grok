"""
The permissions() directive only accepts permission ids or permission classes:

  >>> import grok
  >>> grok.testing.grok('grok.tests.security.not_a_permission_class_fixture')
  Traceback (most recent call last):
  ...
  GrokImportError: You can only pass unicode values, ASCII values, or
  subclasses of grokcore.security.Permission to the 'permissions' directive.

"""
