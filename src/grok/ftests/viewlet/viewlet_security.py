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

Traverse to the view on the model object. We get the viewlets
registered for the default layer, with the anybody permission::

  >>> from zope.testbrowser.testing import Browser
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

Now we traverse to the view through a skin. Now we gain the viewlet registered for a particular layer, ``LayeredBone``::

  >>> browser.open('http://localhost/++skin++boneskin/wilma/@@caveview')
  >>> print browser.contents
  Brack Bone
  Gold Bone
  Layered Bone
  T-Rex Bone

"""


import grok
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class Gold(grok.Permission):
    grok.name('bone.gold')

class CaveWoman(grok.Model):
    pass

class CaveView(grok.View):
    pass

class Pot(grok.ViewletManager):
    grok.name('pot')

class TRexBone(grok.Viewlet):
    grok.viewletmanager(Pot)

    def render(self):
        return "T-Rex Bone"

class BrackerBone(grok.Viewlet):
    grok.viewletmanager(Pot)

    def render(self):
        return "Brack Bone"

class BoneOwner(grok.Role):
    grok.name('grok.BoneOwner')
    grok.title('Bone Ownwer')
    grok.permissions('bone.gold')

class GoldBone(grok.Viewlet):
    grok.viewletmanager(Pot)
    grok.require('bone.gold')

    def render(self):
        return 'Gold Bone'

class IBoneLayer(grok.IGrokLayer, IDefaultBrowserLayer):
    pass

class LayeredBone(grok.Viewlet):
    grok.viewletmanager(Pot)
    grok.layer(IBoneLayer)

    def render(self):
        return 'Layered Bone'

class BoneSkin(grok.Skin):
    grok.layer(IBoneLayer)
