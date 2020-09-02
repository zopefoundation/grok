"""
Views have an application_url() method to easily retrieve the url of the
application::

  >>> getRootFolder()['cave'] = cave = Cave()
  >>> cave['caveman'] = CaveMan()

Asking for the application_url on the cave returns the URL to the cave::

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/cave')
  >>> browser.contents
  'http://localhost/cave'

Asking for the application_url on the caveman returns the URL to the cave as
well::

  >>> browser.open('http://localhost/cave/caveman')
  >>> browser.contents
  'http://localhost/cave'

You can pass a name to specify a particular view or sub object to add
to the URL::

  >>> browser.open('http://localhost/cave/caveman/second')
  >>> browser.contents
  'http://localhost/cave/second'

URLs can be computed for skins too::

  >>> browser.open('http://localhost/cave/caveman/third')
  >>> browser.contents
  'http://localhost/++skin++mammothskin/cave/third'

  >>> browser.open('http://localhost/cave/caveman/fourth')
  >>> browser.contents
  'http://localhost/++skin++mammothskin/cave/fourth?key=value'


application_url also works with empty containers::

  >>> from grok.ftests.url.application import Corridors
  >>> cave['corridors'] = Corridors()
  >>> browser.open('http://localhost/cave/corridors')
  >>> browser.contents
  'http://localhost/cave'

"""
import zope.interface
import grok
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IMarker(zope.interface.Interface):
    pass


class Index(grok.View):
    grok.context(IMarker)

    def render(self):
        return self.application_url()


class Second(grok.View):
    grok.context(IMarker)

    def render(self):
        return self.application_url('second')


@grok.implementer(IMarker)
class Cave(grok.Application, grok.Container):
    pass


@grok.implementer(IMarker)
class CaveMan(grok.Model):
    pass


@grok.implementer(IMarker)
class Corridors(grok.Container):
    pass


class IMammothSkin(IDefaultBrowserLayer):
    grok.skin('mammothskin')


class Third(grok.View):
    grok.context(IMarker)

    def render(self):
        return self.application_url('third', skin=IMammothSkin)


class Fourth(grok.View):
    grok.context(IMarker)

    def render(self):
        return self.application_url(
            'fourth', skin=IMammothSkin, data={'key': 'value'})
