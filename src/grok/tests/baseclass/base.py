"""
Base classes shouldn't be grokked. The way is to use the
'grok.baseclass' directive on the class itself.

  >>> grok.testing.grok(__name__)

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> model = ModelBase()

  >>> view = component.getMultiAdapter((model, request), name='anotherview')
  Traceback (most recent call last):
    ...
  ComponentLookupError: ((<grok.tests.baseclass.base.ModelBase object at 0x...>,
  <zope.publisher.browser.TestRequest instance ...>),
  <InterfaceClass zope.interface.Interface>,
  'anotherview')
  
"""
import grok

class ModelBase(grok.Model):
    pass

class AnotherView(grok.View):
    grok.baseclass()
    
    def render(self):
        return "hello world"
