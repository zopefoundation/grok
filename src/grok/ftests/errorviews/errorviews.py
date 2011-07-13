"""

By default, the views rendered for error situations is handled by
zope.errorviews::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> view = getMultiAdapter((Exception(), TestRequest()), name='index')
  >>> print view()
  A system error occurred.

Error views no longer by default provide ISystemErrorView. It would result in
duplicate log output otherwise.

  >>> from zope.browser.interfaces import ISystemErrorView
  >>> ISystemErrorView.providedBy(view)
  False

  >>> from zope.publisher.interfaces import NotFound
  >>> request = TestRequest()
  >>> error = NotFound(object(), request)
  >>> view = getMultiAdapter((error, request), name='index')
  >>> print view()
  The requested resource can not be found.

  >>> from zope.security.interfaces import Unauthorized
  >>> request = TestRequest()
  >>> request.setPrincipal(MockPrincipal())
  >>> view = getMultiAdapter((Unauthorized(), request), name='index')
  >>> print view()
  Access to the requested resource is forbidden.

The default views can be selectively overridden in your application::

  >>> from grok import ExceptionView
  >>> class MyExceptionView(ExceptionView):
  ...     def render(self):
  ...         return u'This is my idea of an exception view.'
  >>> from grok.testing import grok_component
  >>> grok_component('MyExceptionView', MyExceptionView)
  True

  >>> view = getMultiAdapter((Exception(), TestRequest()), name='index')
  >>> print view()
  This is my idea of an exception view.

  >>> from grok import NotFoundView
  >>> class MyNotFoundView(NotFoundView):
  ...     def render(self):
  ...         return u'This is my idea of a not found view.'
  >>> grok_component('MyNotFoundView', MyNotFoundView)
  True

  >>> request = TestRequest()
  >>> error = NotFound(object(), request)
  >>> view = getMultiAdapter((error, request), name='index')
  >>> print view()
  This is my idea of a not found view.

  >>> from grok import UnauthorizedView
  >>> class MyUnauthorizedView(UnauthorizedView):
  ...     def render(self):
  ...         return u'This is my idea of an unauthorized view.'
  >>> grok_component('MyUnauthorizedView', MyUnauthorizedView)
  True

  >>> request = TestRequest()
  >>> request.setPrincipal(MockPrincipal())
  >>> view = getMultiAdapter((Unauthorized(), request), name='index')
  >>> print view()
  This is my idea of an unauthorized view.

  >>> class WithTemplate(ExceptionView):
  ...     grok.template('exceptionview_template')
  >>> grok_component('WithTemplate', WithTemplate)
  True

  >>> view = getMultiAdapter((Exception(), TestRequest()), name='index')
  >>> print view()
  <html>
  <body>
  <h1>Something went wrong!</h1>
  <p>Exception()</p>
  </body>
  </html>

"""
import grok

class MockPrincipal(object):
    id = 'mockprincipal'

exceptionview_template = grok.PageTemplate("""\
<html>
<body>
<h1>Something went wrong!</h1>
<p tal:content="python: repr(context)"/>
</body>
</html>
""")
