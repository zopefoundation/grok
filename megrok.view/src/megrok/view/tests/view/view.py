"""
  >>> import grok
  >>> from megrok.view.tests.view.view import Mammoth
  >>> grok.grok('megrok.view.tests.view.view')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred/@@painting")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  </body>
  </html>

"""
import grok
import megrok.view

class Mammoth(grok.Model):
    pass

class Painting(megrok.view.View):
    pass

painting = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
</body>
</html>
""")
