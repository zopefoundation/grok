"""
A Role component optionally defines what permission it comprises.

The grok.permissions() directive is used to specify the set of permissions
that are aggregated in the particular Role. The permissions can be referenced
by "name" or by class.

  >>> grok.testing.grok(__name__)
"""

import grok
import zope.interface

class FirstPermission(grok.Permission):
    grok.name('first permission')

class SecondPermission(grok.Permission):
    grok.name('second permission')

class RoleComprisingTwoPermissionsByName(grok.Role):
    grok.name('ByName')
    grok.permissions(
        'first permission',
        'second permission'
        )

class RoleComprisingTwoPermissionsByClass(grok.Role):
    grok.name('ByClass')
    grok.permissions(
        FirstPermission,
        SecondPermission
        )
