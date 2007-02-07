"""
  >>> import grok
  >>> grok.grok('grok.ftests.admin.admin')

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/")
  >>> print browser.contents
  <html>
  ...
  <h1>Installed applications</h1>
  ...
  <legend>Add application</legend>
  ...
  >>> browser.getControl('Application').displayValue = ['grok.ftests.admin.admin.MammothManager']
  >>> browser.getControl('Name').value = 'my-mammoth-manager'
  >>> browser.getControl('Add').click()
  >>> print browser.contents
  <html>
  ...
  <li>
    <a href="http://localhost/my-mammoth-manager">
    my-mammoth-manager
    (MammothManager)
    </a>
  </li>
  ...
  >>> browser.getLink('my-mammoth-manager').click()
  >>> print browser.contents
  Let's manage some mammoths!

"""
import grok

class MammothManager(grok.Application):
    pass

class Index(grok.View):

    def render(self):
        return u"Let's manage some mammoths!"
