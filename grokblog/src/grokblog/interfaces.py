from zope.interface import Interface
from zope import schema, interface

class IEntry(Interface):
    """
    This interface is based on the Atom entry definition, from the Atom RFC.
    
    http://tools.ietf.org/html/rfc4287
    """
    
    # id is generated when we generate entry text
    
    title = schema.TextLine(title=u"Title", required=True)

    updated = schema.Datetime(title=u"Updated", required=True)

    published = schema.Datetime(title=u"Published", required=False)

##     authors = schema.List(title=u"Authors", value_type=schema.Object,
##                           default=[])

##     contributors = schema.List(title=u"Contributors", value_type=schema.Object,
##                                default=[])

##     categories = schema.List(title=u"Categories", value_type=schema.Object,
##                              default=[])
 
    #links = schema.List(title=u"Links", value_type=schema.TextLine,
    #                    default=[])

    summary = schema.SourceText(title=u"Summary", required=False)

    # content = schema.SourceText(title=u"Content")

    rightsinfo = schema.SourceText(title=u"Rights", required=False)

    # source is too complicated to support for us right now

class IRestructuredTextEntry(IEntry):
    content = schema.SourceText(title=u"Content")

class IAtomEntry(Interface):
    
    def xml():
        """Return Atom representation of an entry.
        """

class IAtomContent(Interface):
    def xml():
        """Return Atom representation of content of object.
        """
        
