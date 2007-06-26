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
  ...<legend>Add application</legend>
  ...
  >>> browser.getControl('Application').displayValue = ['grok.ftests.admin.admin.MammothManager']
  >>> browser.getControl('Name').value = 'my-mammoth-manager'
  >>> browser.getControl('Add').click()
  >>> print browser.contents
  <html>
  ...
      <li>
        <input type="checkbox" name="items" value="my-mammoth-manager" />
        <a href="http://localhost/my-mammoth-manager">
          my-mammoth-manager
          (MammothManager)
        </a>
      </li>
  ...
  >>> browser.getLink('my-mammoth-manager').click()
  >>> print browser.contents
  Let's manage some mammoths!

We are able to delete installed applications.

  >>> browser.open("http://localhost/")
  >>> print browser.contents
  <html>
  ...
  ...<legend>Installed applications</legend>
  ...
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='my-mammoth-manager').selected = True
  >>> browser.getControl('Delete Selected').click()
  >>> print browser.contents
  <html>
  ...
  ...<legend>Add application</legend>
  ...

"""
import grok

class MammothManager(grok.Application, grok.Container):
    pass

class Index(grok.View):

    def render(self):
        return u"Let's manage some mammoths!"
