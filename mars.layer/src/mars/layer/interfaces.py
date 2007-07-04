import zope.interface

class IMarsLayerDirectives(zope.interface.Interface):

    def layer(class_or_interface):
        """The layer for which the object should be available.
        Default: zope.publisher.browser.interfaces.IBrowserRequest
        """
