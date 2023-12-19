import grok


class NotAPermissionSubclass:
    grok.name('not really a permission')


class MyRole(grok.Role):
    grok.name('MyRole')
    grok.permissions(NotAPermissionSubclass)
