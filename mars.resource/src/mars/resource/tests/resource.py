"""
Test the claimed directives.

  >>> import grok
  >>> grok.grok('mars.resource.tests.resource')

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> #browser.addHeader('Authorization', 'Basic mgr:mgrpw')

These tests make use of minimal layer

  >>> skinURL = 'http://localhost/++skin++myskin'
  >>> browser.open(skinURL + '/++resource++site.css')
  >>> print browser.contents
  body {
      background-color: white;
      color: black;
  }

  >>> browser.open(skinURL + '/++resource++logo.jpg')

And using the resource directory

  >>> browser.open(skinURL + '/++resource++resources/site.css')
  >>> print browser.contents
  body {
      background-color: white;
      color: black;
  }

"""

import grok
import mars.resource
import mars.layer

class IMyLayer(mars.layer.IMinimalLayer):
    pass

# set layer on module level, all class declarations that use directive
# mars.layer.layer will use this layer - Skin, views, resources and templates
mars.layer.layer(IMyLayer)

class MySkin(mars.layer.Skin):
    pass

# define a file resource
class Style(mars.resource.ResourceFactory):
    grok.name('site.css')
    mars.resource.file('resources/site.css')

# define an image resource
class Logo(mars.resource.ResourceFactory):
    grok.name('logo.jpg')
    mars.resource.file('resources/logo.jpg')

# define a resource directory, takes name from factory.__name__
class Resources(mars.resource.ResourceDirectoryFactory):
    mars.resource.directory('resources')
