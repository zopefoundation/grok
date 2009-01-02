"""
REST objects, like all views, are properly located objects and will
therefore honour local grants, for instance.  Let's consider the
following model in the root folder.

  >>> root = getRootFolder()
  >>> root['manfred'] = manfred = Mammoth('manfred')

For this model we have registered a REST GET view that's protected
with a permission.  Therefore we can't access it as anonymous:

  >>> print http(r'''
  ... GET /++rest++mammoth/manfred HTTP/1.1
  ... ''')
  HTTP/1.1 401 Unauthorized
  Content-Length: 0
  Content-Type: text/plain
  WWW-Authenticate: basic realm="Zope"

However, if we make a (local!) grant, e.g. on the root object, we can
access the view just fine:

  >>> from zope.securitypolicy.interfaces import IPrincipalPermissionManager
  >>> root_perms = IPrincipalPermissionManager(root)
  >>> root_perms.grantPermissionToPrincipal('mammoth.Touch', 'zope.anybody')

With the grant in place we can access it as anonymous:

  >>> print http(r'''
  ... GET /++rest++mammoth/manfred HTTP/1.1
  ... ''')
  HTTP/1.1 200 Ok
  Content-Length: 7
  Content-Type: text/plain
  <BLANKLINE>
  manfred

In fact, inspecting the view object itself, we see that it is a true
ILocation and has the appropriate parent pointer:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest(skin=MammothRestLayer)
  >>> from zope.component import getMultiAdapter
  >>> view = getMultiAdapter((manfred, request), name='GET')

  >>> from zope.location.interfaces import ILocation
  >>> ILocation.providedBy(view)
  True
  >>> view.__parent__ is manfred
  True

"""
import grok

class Mammoth(grok.Model):

    def __init__(self, name):
        self.name = name

class MammothRestLayer(grok.IRESTLayer):
    grok.restskin('mammoth')

class TouchMammoth(grok.Permission):
    grok.name('mammoth.Touch')

class MammothRest(grok.REST):
    grok.layer(MammothRestLayer)

    @grok.require(TouchMammoth)
    def GET(self):
        return self.context.name
