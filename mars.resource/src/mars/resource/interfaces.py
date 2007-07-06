import zope.interface

class IMarsResourceDirectives(zope.interface.Interface):

    def file(path):
        """Path to the resource
        Required for Resource
        """

    def directory(path):
        """Path to the resource directory
        Required for ResourceDirectory
        """

