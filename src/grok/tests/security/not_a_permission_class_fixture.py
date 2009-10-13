import grok

class NotAPermissionSubclass(object):
    grok.name('not really a permission')

class MyRole(grok.Role):
    grok.name('MyRole')
    grok.permissions(NotAPermissionSubclass)
