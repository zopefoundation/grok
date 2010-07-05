"""
Apart from using the ``traverse`` method on a model, you can
also create a separate traverser component:

  >>> getRootFolder()["herd"] = Herd('The Big Mammoth Herd')

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Manfred!</h1>
  <p>Manfred is part of The Big Mammoth Herd.</p>
  </body>
  </html>

  >>> browser.open("http://localhost/herd/ellie")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Ellie!</h1>
  <p>Ellie is part of The Big Mammoth Herd.</p>
  </body>
  </html>

"""
import grok

class Herd(grok.Model):

    def __init__(self, name):
        self.name = name

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
<p><span tal:replace="context/name/title" /> is part of <span tal:replace="context/__parent__/name" />.</p>
</body>
</html>
""")
