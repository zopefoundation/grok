"""
  >>> import grok
  >>> grok.grok('grok.ftests.security.roles')

Viewing a protected view with insufficient privileges will yield
Unauthorized:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.open("http://localhost/@@cavepainting")
  Traceback (most recent call last):
  HTTPError: HTTP Error 401: Unauthorized
  >>> browser.open("http://localhost/@@editcavepainting")
  Traceback (most recent call last):
  HTTPError: HTTP Error 401: Unauthorized
  >>> browser.open("http://localhost/@@erasecavepainting")
  Traceback (most recent call last):
  HTTPError: HTTP Error 401: Unauthorized

When we log in (e.g. as a manager), we can access the views just fine:

  >>> from zope.app.securitypolicy.principalrole import principalRoleManager
  >>> principalRoleManager.assignRoleToPrincipal(
  ...    'grok.PaintingOwner', 'zope.mgr')
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.open("http://localhost/@@cavepainting")
  >>> print browser.contents
  What a beautiful painting.

  >>> browser.open("http://localhost/@@editcavepainting")
  >>> print browser.contents
  Let's make it even prettier.

  >>> browser.open("http://localhost/@@erasecavepainting")
  >>> print browser.contents
  Oops, mistake, let's erase it.

  >>> browser.open("http://localhost/@@approvecavepainting")
  Traceback (most recent call last):
  HTTPError: HTTP Error 403: Forbidden
"""

import grok
import zope.interface

class View(grok.Permission):
    id = 'grok.ViewPainting'
    title = u'View Painting'

class Edit(grok.Permission):
    id = 'grok.EditPainting'
    title = u'Edit Painting'

class Erase(grok.Permission):
    id = 'grok.ErasePainting'
    title = u'Erase Painting'

class Approve(grok.Permission):
    id = 'grok.ApprovePainting'
    title = u'Approve Painting'

class PaintingOwner(grok.Role):
    id = 'grok.PaintingOwner'
    title = u'Painting Owner'
    grok.permissions(
        'grok.ViewPainting', 'grok.EditPainting', 'grok.ErasePainting')

class CavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require('grok.ViewPainting')

    def render(self):
        return 'What a beautiful painting.'

class EditCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require('grok.EditPainting')

    def render(self):
        return 'Let\'s make it even prettier.'

class EraseCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require('grok.ErasePainting')

    def render(self):
        return 'Oops, mistake, let\'s erase it.'

class ApproveCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require('grok.ApprovePainting')

    def render(self):
        return 'Painting owners cannot approve their paintings.'
