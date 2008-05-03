"""
When you call the grok.local_utility directive multiple times specifying
the same (interface, name) combination, we expect an error:

  >>> import grok.tests.utility.multiple_directive_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: ("Conflicting local utility registration
  <class 'grok.tests.utility.multiple_directive_fixture.Fireplace2'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grok.tests.utility.multiple_directive_fixture.IFireplace>
  and name u''.",
  <class 'grok.tests.utility.multiple_directive_fixture.Fireplace2'>)
"""
