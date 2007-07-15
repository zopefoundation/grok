import grok
from zope import interface, schema

class IBook(interface.Interface):
    title = schema.TextLine(title=u"Title", required=True)

class Book(grok.Model):
    """
    A simple book with a title.

    >>> book = Book()
    >>> book.title
    >>> book.title = "Web Component Development with Zope 3"
    >>> book.title
    'Web Component Development with Zope 3'

    """
    interface.implements(IBook)
    title = ''

    def __init__(self, title=None):
        super(Book, self).__init__()
        self.title = title

class Edit(grok.EditForm):
    pass

class Index(grok.DisplayForm):
    pass
