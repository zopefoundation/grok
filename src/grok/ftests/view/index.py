"""
  >>> getRootFolder()["manfred"] = Mammoth()

The default view name for a model is 'index':

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  <span>Blue</span>
  <span>Blue</span>
  </body>
  </html>

"""
import grok

class Mammoth(grok.Model):
    teeth = u"Blue"

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
<span tal:content="python:context.teeth">green</span>
<span tal:content="context/teeth">green</span>
</body>
</html>
""")
