"""
  >>> import grok
  >>> from grok.ftests.view.layer import Mammoth
  >>> grok.grok('grok.ftests.view.layer')
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
  
  >>> browser.open("http://localhost/++skin++Rotterdam/manfred/@@cavedrawings")
  Traceback (most recent call last):
  ...
  NotFound: Object: <grok.ftests.view.layer.Mammoth object at ...>, name: u'@@cavedrawings'
  >>> browser.open("http://localhost/++skin++Rotterdam/manfred/@@moredrawings")
  >>> print browser.contents
  Pretty

  #>>> browser.open("http://localhost/++skin++MySkin/manfred/@@evenmoredrawings")
  #>>> print browser.contents
  #Awesome

"""
import grok
from zope.app.basicskin import IBasicSkin
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.rotterdam import rotterdam
from zope import interface

grok.layer(IBasicSkin)

class MySkinLayer(grok.ILayer):
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
    grok.layer(MySkin)

    def render(self):
        return "Awesome"
