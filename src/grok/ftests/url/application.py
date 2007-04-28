"""
Views have an application_url() method to easily retrieve the url of the
application::

  >>> import grok
  >>> grok.grok('grok.ftests.url.application')

  >>> from grok.ftests.url.application import Cave, CaveMan
  >>> getRootFolder()['cave'] = cave = Cave()
  >>> cave['caveman'] = CaveMan()

Asking for the application_url on the cave returns the URL to the cave::

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/cave')
  >>> browser.url
  'http://localhost/cave'

Asking for the application_url on the caveman returns the URL to the cave as
well::

  >>> browser.open('http://localhost/cave/caveman')
  >>> browser.url
  'http://localhost/cave/caveman'

"""
import zope.interface

import grok


class Index(grok.View):
    grok.context(zope.interface.Interface)

    def render(self):
        return self.application_url()


class Cave(grok.Application, grok.Container):
    pass


class CaveMan(grok.Model):
    pass
