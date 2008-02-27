"""
  >>> getRootFolder()["manfred"] = Mammoth()
 
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/++skin++Basic/manfred/@@cavedrawings")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  </body>
  </html>
  
  >>> browser.open("http://localhost/++skin++Rotterdam/manfred/@@moredrawings")
  >>> print browser.contents
  Pretty

  >>> browser.open("http://localhost/++skin++myskin/manfred/@@evenmoredrawings")
  >>> print browser.contents
  Awesome

"""
import grok
from zope.app.basicskin import IBasicSkin
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.rotterdam import rotterdam
from zope import interface

grok.layer(IBasicSkin)

class MySkinLayer(grok.IGrokLayer):
    pass

class MySkin(grok.Skin):
    grok.layer(MySkinLayer)

class Mammoth(grok.Model):
    pass

class CaveDrawings(grok.View):
    pass

cavedrawings = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
</body>
</html>
""")

class MoreDrawings(grok.View):
    grok.layer(rotterdam)

    def render(self):
        return "Pretty"


class EvenMoreDrawings(grok.View):
    grok.layer(MySkinLayer)

    def render(self):
        return "Awesome"
