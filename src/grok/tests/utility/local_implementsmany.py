"""
Anything can be registered as a local utility. If it implements a single
interface, there is no need to specify which interface it provides.

In this test, the utility implements more than one interface, so it cannot be
registered as a local utility.

  >>> import grok.tests.utility.local_implementsmany_fixture
  Traceback (most recent call last):
    ...
  GrokError: <class 'grok.tests.utility.local_implementsmany_fixture.Fireplace'>
  is implementing more than one interface (use grok.provides to specify
  which one to use).

"""
