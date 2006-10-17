"""
  >>> import grok
  >>> from grok.ftests.view.index import Mammoth
  >>> grok.grok('grok.ftests.view.index')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  </body>
  </html>

"""
import grok

class Mammoth(grok.Model):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
</body>
</html>
""")
