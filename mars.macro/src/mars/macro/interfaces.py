import zope.interface

class IMarsMacroDirectives(zope.interface.Interface):

    def view(name):
        """The name of the macro to be used. This allows us to reference 
        the named  macro defined with metal:define-macro if we use a 
        different IMacroDirective name.
        Default: empty
        """

    def macro(name):
        """The name of the macro to be used. This allows us to reference 
        the named  macro defined with metal:define-macro if we use a 
        different IMacroDirective name.
        Default: empty
        """

    def content_type(name):
        """The content type identifies the type of data.
        Default: text/html
        """

