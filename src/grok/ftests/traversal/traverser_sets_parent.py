"""
A traverser can set the __parent__ (and __name__) attributes itself,
in which case Grok's traverser won't interfere:

  >>> getRootFolder()["herd"] = Herd('The Big Mammoth Herd')

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Manfred!</h1>
  <p>Manfred is part of The Three Stooges.</p>
  </body>
  </html>

  >>> browser.open("http://localhost/herd/ellie")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, Ellie!</h1>
  <p>Ellie is part of The Three Stooges.</p>
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
        mammoth = Mammoth(name)
        # We pretend the mammoth is the child object of some competely
        # differnt Herd object.
        mammoth.__parent__ = Herd('The Three Stooges')
        return mammoth

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
