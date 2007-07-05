import zope.interface

class IMarsViewletDirectives(zope.interface.Interface):

    def manager(class_or_interface):
        """The manager for which the viewlet is registered
        Default: zope.viewlet.interfaces.IViewletManager
        """

    def view(class_or_interface):
        """The view for which the viewlet is registered
        Default: zope.publisher.browser.interfaces.IBrowserView
        """
