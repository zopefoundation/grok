"""
Apart from using the ``traverse`` method on a model, you can
also create a separate traverser component:

  >>> import grok
  >>> from grok.ftests.traversal.traverser import Herd
  >>> grok.grok('grok.ftests.traversal.traverser')
  >>> getRootFolder()["herd"] = Herd()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Manfred!</h1>
  </body>
  </html>

  >>> browser.open("http://localhost/herd/ellie")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Ellie!</h1>
  </body>
  </html>

"""
import grok

class Herd(grok.Model):
    pass

class HerdTraverser(grok.Traverser):
    grok.context(Herd)

    def traverse(self, name):
        return Mammoth(name)

class Mammoth(grok.Model):

    def __init__(self, name):
        self.name = name

grok.context(Mammoth)

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, <span tal:replace="context/name/title" />!</h1>
</body>
</html>
""")
