from zope.traversing.namespace import skin
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IBrowserRequest

class IDefaultRestLayer(IBrowserRequest):
    pass

class IRestSkinType(IInterface):
    """Skin for REST requests.
    """

class rest_skin(skin):
    skin_type = IRestSkinType

    #def traverse(self, name, ignored):
    #    import pdb; pdb.set_trace()
    #    return super(rest_skin, self).traverse(name, ignored)
    

        
