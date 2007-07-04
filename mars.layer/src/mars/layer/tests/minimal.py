"""

  >>> import grok
  >>> grok.grok('mars.layer.tests.minimal')

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

  >>> skinURL = 'http://localhost/++skin++myskin'

Try opening page.htm which is registered in ftesting.zcml for
z3c.layer.IMinimalBrowserLayer.

  >>> browser.open(skinURL + '/page.html')
  >>> print browser.contents
  <BLANKLINE>
  <html>
  <head>
    <title>testing</title>
  </head>
  <body>
  <BLANKLINE>
    test page
  <BLANKLINE>
  </body>
  </html>
  <BLANKLINE>
  <BLANKLINE>


"""

import grok
import mars.layer

class IMyLayer(mars.layer.IMinimalLayer):
    pass

class MySkin(mars.layer.Skin):
    mars.layer.layer(IMyLayer)

