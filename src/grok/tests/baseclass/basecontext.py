"""
A base class of something that can be a context (such as a model) can
function as a module-level context, and thus can have views associated
with it.

  >>> grok.grok(__name__)

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> model = ModelBase()
  >>> view = component.getMultiAdapter((model, request), name='viewbase')
  Traceback (most recent call last):
    ...
  ComponentLookupError: ((<grok.tests.baseclass.basecontext.ModelBase object at 0x...>,
  <zope.publisher.browser.TestRequest instance ...>),
  <InterfaceClass zope.interface.Interface>,
  'viewbase')
  >>> view = component.getMultiAdapter((model, request), name='realview')
  >>> view.render()
  'hello world'
"""

import grok

class ModelBase(grok.Model):
    pass

class ViewBase(grok.View):    
    def render(self):
        return "hello world"

class RealView(ViewBase):
    pass
