import zope.interface

class IMarsViewDirectives(zope.interface.Interface):

    def layout(name):
        """Declare the layout name for a view.
        If defined the layout will be looked up as a named adapter.
        Should only be defined if the layout template has been registered as a named
        adapter.
        """

