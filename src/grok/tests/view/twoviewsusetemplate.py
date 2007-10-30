"""
A template can be used by multiple views at the same time:

  >>> grok.testing.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component

  >>> view = component.getMultiAdapter((manfred, request), name='a')
  >>> print view()
  View A

  >>> view = component.getMultiAdapter((manfred, request), name='b')
  >>> print view()
  View A

It also works if templates are both associated explicitly:

  >>> view = component.getMultiAdapter((manfred, request), name='c')
  >>> print view()
  Template

  >>> view = component.getMultiAdapter((manfred, request), name='d')
  >>> print view()
  Template

Because the template is associated, we do not expect it to be
registered as its own view:

  >>> view = component.getMultiAdapter((manfred, request), name='templ')
  Traceback (most recent call last):
    ...
  ComponentLookupError:
  ((<grok.tests.view.twoviewsusetemplate.Mammoth object at 0x...>,
  <zope.publisher.browser.TestRequest instance URL=http://127.0.0.1>),
  <InterfaceClass zope.interface.Interface>, 'templ')


"""
import grok

class Mammoth(grok.Model):
    pass

class A(grok.View):
    pass

a = grok.PageTemplate("View A")

class B(grok.View):
    grok.template('a')

class C(grok.View):
    grok.template('templ')

class D(grok.View):
    grok.template('templ')

templ = grok.PageTemplate('Template')
