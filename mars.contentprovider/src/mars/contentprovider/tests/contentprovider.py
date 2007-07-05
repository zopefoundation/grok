"""
  >>> import grok
  >>> grok.grok('mars.contentprovider.tests.contentprovider')
  >>> from mars.contentprovider.tests.contentprovider import Mammoth
  >>> getRootFolder()["mammoth"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> skinURL = 'http://localhost/++skin++myskin'
  >>> browser.open(skinURL + '/mammoth/@@index')
  >>> print browser.contents
  <div>
  I am Manfred the Mammoth
  </div>

"""

import grok
import mars.view
import mars.layer
import mars.template
import mars.contentprovider

class IMySkinLayer(mars.layer.IMinimalLayer):
    pass

# layer used for all registrations in this module
mars.layer.layer(IMySkinLayer)

class MySkin(mars.layer.Skin):
    pass

class Mammoth(grok.Model):
    title = u'Manfred'

class Index(mars.view.LayoutView):
    pass

class IndexLayout(mars.template.LayoutFactory):
    grok.template('index.pt')
    grok.context(Index)

class Title(mars.contentprovider.ContentProvider):

    def render(self):
        return self.context.title

