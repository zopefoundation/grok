"""
Let's test whether require decorators work for json methods.

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()

We can access the public method just fine::

  >>> browser.open('http://localhost/stomp')
  >>> print(browser.contents)
  b'{"Manfred stomped.": ""}'

We cannot access the protected method however::

  >>> # Work around https://github.com/python/cpython/issues/90113
  >>> browser.raiseHttpErrors = False
  >>> browser.open('http://localhost/dance')
  >>> print(browser.headers['status'])
  401 Unauthorized


Let's log in as the manager now. We should be able to access the method now::

  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/dance')
  >>> print(browser.contents)
  b'{"Manfred doesn\\'t like to dance.": ""}'

"""

import zope.interface

import grok


class MammothJSON(grok.JSON):
    grok.context(zope.interface.Interface)

    def stomp(self):
        return {'Manfred stomped.': ''}

    @grok.require('zope.ManageContent')
    def dance(self):
        return {'Manfred doesn\'t like to dance.': ''}
