"""
Viewing a protected view with insufficient privileges will yield
Unauthorized:

  >>> from zope.testbrowser.wsgi import Browser
  >>> browser = Browser()
  >>> # Work around https://github.com/python/cpython/issues/90113
  >>> browser.raiseHttpErrors = False

  >>> browser.open("http://localhost/@@cavepainting")
  >>> print(browser.headers['status'])
  401 Unauthorized

  >>> browser.open("http://localhost/@@editcavepainting")
  >>> print(browser.headers['status'])
  401 Unauthorized

  >>> browser.open("http://localhost/@@erasecavepainting")
  >>> print(browser.headers['status'])
  401 Unauthorized

Let's now grant anonymous the PaintingOwner role locally (so that we
don't have to modify the global setup).  Then we can access the views
just fine:

  >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager
  >>> root = getRootFolder()
  >>> IPrincipalRoleManager(root).assignRoleToPrincipal(
  ...    'paint.PaintingOwner', 'zope.anybody')

  >>> browser.open("http://localhost/@@cavepainting")
  >>> print(browser.contents)
  What a beautiful painting.

  >>> browser.open("http://localhost/@@editcavepainting")
  >>> print(browser.contents)
  Let's make it even prettier.

  >>> browser.open("http://localhost/@@erasecavepainting")
  >>> print(browser.contents)
  Oops, mistake, let's erase it.

  >>> browser.open("http://localhost/@@approvecavepainting")
  >>> print(browser.headers['status'])
  401 Unauthorized
"""

import zope.interface

import grok


class ViewPermission(grok.Permission):
    grok.name('paint.ViewPainting')


class EditPermission(grok.Permission):
    grok.name('paint.EditPainting')


class ErasePermission(grok.Permission):
    grok.name('paint.ErasePainting')


class ApprovePermission(grok.Permission):
    grok.name('paint.ApprovePainting')


class PaintingOwner(grok.Role):
    grok.name('paint.PaintingOwner')
    grok.title('Painting Owner')
    grok.permissions(
        'paint.ViewPainting', 'paint.EditPainting', 'paint.ErasePainting')


class CavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(ViewPermission)

    def render(self):
        return 'What a beautiful painting.'


class EditCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(EditPermission)

    def render(self):
        return 'Let\'s make it even prettier.'


class EraseCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(ErasePermission)

    def render(self):
        return 'Oops, mistake, let\'s erase it.'


class ApproveCavePainting(grok.View):

    grok.context(zope.interface.Interface)
    grok.require(ApprovePermission)

    def render(self):
        return 'Painting owners cannot approve their paintings.'
