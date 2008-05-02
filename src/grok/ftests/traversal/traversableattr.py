"""
Models can determine how they want to be traversed by
implementing a 'traverse' method:

  >>> getRootFolder()["traversefoo"] = TraFoo('foo')

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/traversefoo/")
  >>> print browser.contents
  <html>
  <body>foo</body>
  </html>
  >>> browser.open("http://localhost/traversefoo/foo")
  >>> print browser.contents
  foo
  >>> browser.open("http://localhost/traversefoo/bar")
  >>> print browser.contents
  <html>
  <body>bar</body>
  </html>


"""
import grok

class TraBar(grok.Model):
    def __init__(self, name):
        self.name = name

#class TraBarIndex(grok.View):
#    grok.context(TraBar)
#    def render(self):
#        return self.name

class TraFoo(grok.Model): #, grok.Application):
    grok.traversable('bar')
    grok.traversable('foo')

    def __init__(self, name):
        self.name = name

    foo = TraBar('foo')
    def bar(self):
        return TraBar('bar')

#class TraFooIndex(grok.View):
#    grok.context(TraFoo)
#    def render(self):
#        return self.name
