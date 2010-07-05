"""

=============
Test Viewlets
=============

This doctest will test the various grok viewlet registrations. Grok
viewlets offer the same flexibility as zope3, allowing you to register
viewlets for a particular view, context, layer, and permission.

Set up a content object in the application root::

  >>> root = getRootFolder()
  >>> root['wilma'] = CaveWoman()
  >>> root['fred'] = CaveMan()

Traverse to the view on the model object. We get the viewlets
registered for the default layer, with the anybody permission::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/wilma/@@caveview")
  >>> print browser.contents
  Brack Bone
  T-Rex Bone

After assigning the ``grok.BoneOwner`` role to ``zope.anybody``, he
gains the ``bone.gold`` permission. This allows the principal to view
the ``GoldBone`` viewlet::

  >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager
  >>> IPrincipalRoleManager(root).assignRoleToPrincipal(
  ...    'grok.BoneOwner', 'zope.anybody')
  >>> browser.open("http://localhost/wilma/@@caveview")
  >>> print browser.contents
  Brack Bone
  Gold Bone
  T-Rex Bone

Now we traverse to the view through a skin. We gain the viewlet
registered for a particular layer, ``LayeredBone``::

  >>> browser.open('http://localhost/++skin++boneskin/wilma/@@caveview')
  >>> print browser.contents
  Brack Bone
  Gold Bone
  Layered Bone
  T-Rex Bone

Only viewlets registered for the CaveMan model, ``ManBone``, should up
when traversing to fred::

  >>> browser.open('http://localhost/fred/@@caveview')
  >>> print browser.contents
  Brack Bone
  Gold Bone
  Man Bone
  T-Rex Bone


Viewlets registered for a particular view, like ``LadyViewlet``,
should only associate with that particular one::

  >>> browser.open('http://localhost/fred/@@fireview')
  >>> print browser.contents
  Brack Bone
  Gold Bone
  Lady Viewlet
  Man Bone
  T-Rex Bone

Viewlets and viewlet managers should have a __name__. It's used
for instance when looking up the absolute url for the viewlet
or manager.

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> model = CaveWoman()
  >>> view = CaveView(model, request)

Managers and viewlets should get their  name from the class name
if grok.name() is not present.

  >>> manager = Pot(model, request, view)
  >>> manager.__name__
  'pot'
  >>> viewlet = BrackerBone(model, request, view, manager)
  >>> viewlet.__name__
  'brackerbone'

If grok.name() is specified for manager and viewlet they should
get those names.

  >>> manager = NamedViewletManager(model, request, view)
  >>> manager.__name__
  'managerwithname'
  >>> viewlet = NamedViewlet(model, request, view, manager)
  >>> viewlet.__name__
  'viewletwithname'

"""


import grok
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class Gold(grok.Permission):
    grok.name('bone.gold')

class CaveWoman(grok.Model):
    pass

class CaveMan(grok.Model):
    pass

class CaveView(grok.View):
    grok.context(Interface)

class FireView(grok.View):
    grok.context(Interface)
    grok.template('caveview')

class Pot(grok.ViewletManager):
    grok.context(Interface)
    grok.name('pot')

class TRexBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Pot)

    def render(self):
        return "T-Rex Bone"

class BrackerBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Pot)

    def render(self):
        return "Brack Bone"

class BoneOwner(grok.Role):
    grok.name('grok.BoneOwner')
    grok.title('Bone Ownwer')
    grok.permissions('bone.gold')

class GoldBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Pot)
    grok.require(Gold)

    def render(self):
        return 'Gold Bone'

class IBoneLayer(IDefaultBrowserLayer):
    grok.skin('boneskin')

class LayeredBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Pot)
    grok.layer(IBoneLayer)

    def render(self):
        return 'Layered Bone'

class ManBone(grok.Viewlet):
    grok.viewletmanager(Pot)
    grok.context(CaveMan)

    def render(self):
        return "Man Bone"

class LadyViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Pot)
    grok.view(FireView)

    def render(self):
        return 'Lady Viewlet'

class NamedViewletManager(grok.ViewletManager):
    grok.context(Interface)
    grok.name('managerwithname')

class NamedViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.name('viewletwithname')
    grok.viewletmanager(NamedViewletManager)

    def render(self):
        return "NamedViewlet"

