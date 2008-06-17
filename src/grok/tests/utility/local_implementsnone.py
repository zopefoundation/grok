"""
Anything can be registered as a local utility. If it implements a single
interface, there is no need to specify which interface it provides.

In this test, the utility does not implement any interface, so it cannot be
registered as a local utility.

  >>> import grok.tests.utility.local_implementsnone_fixture
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.utility.local_implementsnone_fixture.Fireplace'>
  must implement at least one interface (use grok.implements to specify).

"""
