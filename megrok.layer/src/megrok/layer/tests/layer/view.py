"""
  >>> import grok
  >>> from megrok.layer.tests.layer.view import Mammoth
  >>> grok.grok('megrok.layer.tests.layer.view')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/++skin++Basic/manfred/cavedrawings")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  </body>
  </html>
  

  >>> browser.open("http://localhost/++skin++Rotterdam/manfred/cavedrawings")
  Traceback (most recent call last):
  ...
  NotFound: Object: <megrok.layer.tests.layer.view.Mammoth object at ...>, name: u'cavedrawings'

  >>> browser.open("http://localhost/++skin++Rotterdam/manfred/moredrawings")
  >>> print browser.contents
  Pretty

  >>> browser.open("http://localhost/++skin++myskin/manfred/evenmoredrawings")
  >>> print browser.contents
  Awesome

"""
import grok
from zope.app.basicskin import IBasicSkin
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.rotterdam import rotterdam
from zope import interface

import megrok.layer
import megrok.view
megrok.layer.layer(IBasicSkin)

class MySkinLayer(megrok.layer.IMinimalLayer):
    pass

class MySkin(megrok.layer.Skin):
    megrok.layer.layer(MySkinLayer)

class Mammoth(grok.Model):
    pass

class CaveDrawings(megrok.view.View):
    pass

cavedrawings = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
</body>
</html>
""")

class MoreDrawings(megrok.view.View):
    megrok.layer.layer(rotterdam)

    def render(self):
        return "Pretty"

class EvenMoreDrawings(megrok.view.View):
    megrok.layer.layer(MySkinLayer)

    def render(self):
        return "Awesome"

