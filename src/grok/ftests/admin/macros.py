##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Macros for the grok admin UI

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open('http://localhost/applications')

Check, that the macros template renders correctly, even if not called
with context of a GAIA object. This is important, because the macro
view is bound to ``Interface`` and can therefore be called with nearly
every object as context.

We create a non-GAIA object, a mammoth called 'manfred'.

  >>> subform = browser.getForm(name='Mammoth')
  >>> subform.getControl('Name your new app:').value = 'manfred'
  >>> subform.getControl('Create').click()

and call the macroview with it:

  >>> browser.open('http://localhost/manfred/@@externalview')
  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
     This template (grokadminmacros.pt in grok.admin) must be called
     from a view with defined root_url.
  ...

So developers get informed, that they called the wrong macro view.

Let's clean up.

  >>> browser.open('http://localhost/applications')
  >>> ctrl = browser.getControl(name='items')
  >>> ctrl.getControl(value='manfred').selected = True
  >>> browser.getControl('Delete Selected').click()


"""
import grok

class Mammoth(grok.Application, grok.Container):
    pass

class ExternalView(grok.View):
    """A view that calls grokadminmacros 'illegally'.
    """
    grok.context(Mammoth)

externalview = grok.PageTemplate("""\
<html metal:use-macro="context/@@grokadminmacros/gaia-page">
</html>
""")

