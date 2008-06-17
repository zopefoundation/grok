"""

The JSON grokker registers a view for each method of the JSON class.
So we should be able to search for view by method name.

  >>> grok.testing.grok(__name__)
  >>> mammoth = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope.component import getMultiAdapter
  >>> view = getMultiAdapter((mammoth, request), name='run')

The 'run' method/view returns json data, but it looks just like python.

  >>> view()
  '{"me": "grok"}'

Let's try calling another method::

  >>> view = getMultiAdapter((mammoth, request), name='another')
  >>> view()
  '{"another": "grok"}'

Although principally all methods of the JSON class are registered as views,
methods with names that start with an underscore are not::

  >>> view = getMultiAdapter((mammoth, request), name='_private')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.view_lookup.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, '_private')

Even more important, special methods like __call__ are not registered
as views either. This test is here to make sure a previous bug has
been fixed::

  >>> view = getMultiAdapter((mammoth, request), name='__call__')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.view_lookup.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, '__call__')

For JSON views we also need to confirm some methods that are defined on the
baseclass (BrowserPage) are not registered as views::

  >>> view = getMultiAdapter((mammoth, request), name='browserDefault')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.view_lookup.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, 'browserDefault')

  >>> view = getMultiAdapter((mammoth, request), name='publishTraverse')
  Traceback (most recent call last):
  ...
  ComponentLookupError: ((<grok.tests.json.view_lookup.Mammoth object at ...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, 'publishTraverse')

"""
import grok

class Mammoth(grok.Model):
    pass

class MammothView(grok.JSON):
    grok.context(Mammoth)

    def run(self):
        return { 'me': 'grok' }

    def another(self):
        return { 'another': 'grok'}

class SecondMammothView(grok.JSON):
    grok.context(Mammoth)

    def _private(self):
        return {'should': 'not be registered'}

    def public(self):
        return {'will': 'be registered'}
