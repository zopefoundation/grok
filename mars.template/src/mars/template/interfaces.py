import zope.interface

class IMarsTemplateDirectives(zope.interface.Interface):

    def macro(name):
        """The macro to be used.  This allows us to define different macros in on template.
        The template designer can now create whole site, the ViewTemplate can then
        extract the macros for single viewlets or views.  If no macro is given the whole
        template is used for rendering.
        Default: empty
        """

    def content_type(name):
        """The content type identifies the type of data.
        Default: text/html
        """

