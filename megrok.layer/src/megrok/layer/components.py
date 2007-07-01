from zope.publisher.interfaces.browser import IBrowserRequest
from z3c.layer.pagelet import IPageletBrowserLayer
from z3c.layer.minimal import IMinimalBrowserLayer

class ILayer(IBrowserRequest):
    pass

class IMinimalLayer(IMinimalBrowserLayer):
    pass

class IPageletLayer(IPageletBrowserLayer):
    pass

class Skin(object):
    pass

