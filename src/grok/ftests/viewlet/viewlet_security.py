"""

Test Viewlets
=============

  >>> root = getRootFolder()
  >>> root['wilma'] = CaveWoman()
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/wilma/@@caveview")
  >>> print browser.contents
  Brack Bone
  T-Rex Bone

  >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager
  >>> IPrincipalRoleManager(root).assignRoleToPrincipal(
  ...    'grok.BoneOwner', 'zope.anybody')
  >>> browser.open("http://localhost/wilma/@@caveview")
  >>> print browser.contents
  Brack Bone
  Gold Bone
  T-Rex Bone

  >> browser.open('http://localhost/++skin++boneskin/wilma/@@caveview')
  >> print browser.contents
  Layered Bone

"""


import grok


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

class IBoneLayer(grok.IGrokLayer):
    pass

class LayeredBone(grok.Viewlet):
    grok.viewletmanager(Pot)
    grok.layer(IBoneLayer)

    def render(self):
        return 'Layered Bone'

class BoneSkin(grok.Skin):
    grok.layer(IBoneLayer)
