"""
Grok views provide `IGrokSecurityView` are handled more openly by the
Grok publisher.

We create an app::

  >>> root = getRootFolder()
  >>> root['app'] = App()

Now we can look at the view::

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser(wsgi_app=wsgi_app())
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/app/@@index')
  >>> print(browser.contents)
  Hello world

"""
import grok

class App(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def render(self):
        return "Hello world"
