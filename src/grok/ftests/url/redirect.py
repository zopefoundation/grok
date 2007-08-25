"""
Views have a redirect() method to easily create redirects:

  >>> getRootFolder()['manfred'] = manfred = Mammoth()

Since the index view redirects to mammoth, we expect to see the URL
point to mammoth:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/manfred')
  >>> browser.url
  'http://localhost/manfred/another'
  
"""
import grok

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    def render(self):
        self.redirect(self.url('another'))

class Another(grok.View):
    def render(self):
        return "Another view"
    

