# -*- coding: latin-1 -*-
"""
We can define a few permissions with grok.Permission and then take a
look at them in Zope 3's grant view:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open("http://localhost/@@grant.html")

  >>> browser.getControl(name='field.principal.MA__.searchstring').value = 'manager'
  >>> browser.getControl('Search').click()
  >>> browser.getControl('Apply').click()
  >>> 'grok.ascii-permission' in browser.contents
  True

"""
import grok

class ASCIIPermission(grok.Permission):
    grok.name('grok.ascii-permission')

# TODO Technically, it's absolutely possible to give permissions
# non-ASCII names. However the way Zope 3's grant view uses widgets to
# display form controls for each permission is not unicode-safe.
