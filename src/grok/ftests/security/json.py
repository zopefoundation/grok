"""
Let's test whether require decorators work for json methods.

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

We can access the public method just fine::

  >>> browser.open('http://localhost/stomp')
  >>> print browser.contents
  {"Manfred stomped.": ""}

We cannot access the protected method however::

  >>> browser.open('http://localhost/dance')
  Traceback (most recent call last):
    ...
  Unauthorized: (<grok.meta.MammothJSON object at ...>, '__call__', 'zope.ManageContent')

Let's log in as the manager now. We should be able to access the method now::

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/dance')
  >>> print browser.contents
  {"Manfred doesn't like to dance.": ""}
  
"""

import grok
import zope.interface

class MammothJSON(grok.JSON):
    grok.context(zope.interface.Interface)

    def stomp(self):
        return {'Manfred stomped.': ''}

    @grok.require('zope.ManageContent')
    def dance(self):
        return {'Manfred doesn\'t like to dance.': ''}
