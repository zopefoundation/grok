"""
When you try to register multiple classes with the same (interface, name)
combination multiple times using grok.local_utility, we expect an error:

  >>> import grok.tests.utility.multiple_class_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: ("Conflicting local utility registration
  <class 'grok.tests.utility.multiple_class_fixture.Fireplace2'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.tests.utility.multiple_class_fixture.IFireplace>
  and name 'Foo'.",
  <class 'grok.tests.utility.multiple_class_fixture.Fireplace2'>)
"""
