"""
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

Form variables such as GET parameters are dispatched to arguments of
the render() method, should the method choose to take them:

  >>> browser.open("http://localhost/manfred/render?message=Foo&another=Bar")
  >>> print browser.contents
  Message: Foo
  Another: Bar

Supplying more arguments than those specified has no effect:

  >>> browser.open("http://localhost/manfred/render?message=There&another=Is&last=More")
  >>> print browser.contents
  Message: There
  Another: Is

If you don't supply all of the arguments, there will be a System Error:

  >>> browser.open("http://localhost/manfred/render?message=Foo")
  Traceback (most recent call last):
  ...
  TypeError: Missing argument to render(): another

The same works with views that define update():

  >>> browser.open("http://localhost/manfred/update?message=Foo&another=Bar")
  >>> print browser.contents
  Coming to us from update():
  Message: Foo
  Another: Bar

  >>> browser.open("http://localhost/manfred/update?message=There&another=Is&last=More")
  >>> print browser.contents
  Coming to us from update():
  Message: There
  Another: Is

  >>> browser.open("http://localhost/manfred/update?another=Bar")
  Traceback (most recent call last):
  ...
  TypeError: Missing argument to update(): message

"""
import grok

class Mammoth(grok.Model):
    pass

class RenderWithArguments(grok.View):
    grok.name('render')

    def render(self, message, another):
        return "Message: %s\nAnother: %s" % (message, another)

class UpdateWithArguments(grok.View):
    grok.name('update')
    grok.template('update')

    def update(self, message, another):
        self.message = message
        self.another = another

update = grok.PageTemplate("""
Coming to us from update():
Message: <span tal:replace="view/message" />
Another: <span tal:replace="view/another" />
""")
