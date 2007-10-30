"""
The baseclass directive can be used to mark something a base class. Of course
subclasses shouldn't inherit this otherwise there is no way to turn them
into non-base classes.

  >>> grok.testing.grok(__name__)

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> model = Model()

We can't look up SomeView as a view, as it's a base class:

  >>> view = component.getMultiAdapter((model, request), name='someview')
  Traceback (most recent call last):
    ...
  ComponentLookupError: ((<grok.tests.baseclass.basedirective.Model object at 0x...>,
  <zope.publisher.browser.TestRequest instance ...>),
  <InterfaceClass zope.interface.Interface>,
  'someview')

We can however get a subclass of SomeView:

  >>> view = component.getMultiAdapter((model, request), name='anotherview')
  >>> view.render()
  'hello world'
"""
import grok

class Model(grok.Model):
    pass

class SomeView(grok.View):
    grok.baseclass()
    
    def render(self):
        return "hello world"

class AnotherView(SomeView):
    pass

