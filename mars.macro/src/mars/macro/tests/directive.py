"""
Test the claimed directives.

  >>> import grok
  >>> grok.grok('mars.macro.tests.directive')

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

"""

import grok
import mars.macro

