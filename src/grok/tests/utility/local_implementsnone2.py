"""
  >>> import grok.tests.utility.local_implementsnone2_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: ("Cannot determine which interface to use for utility
  registration of
  <class 'grok.tests.utility.local_implementsnone2_fixture.Fireplace'>.
  It implements an interface that is a specialization of an interface
  implemented by grok.LocalUtility. Specify the interface by either
  using grok.provides on the utility or passing 'provides' to
  grok.local_utility.",
  <class 'grok.tests.utility.local_implementsnone2_fixture.Fireplace'>)

"""
