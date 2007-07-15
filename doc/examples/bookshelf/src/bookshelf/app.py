import grok
from grok import index
from bookshelf.shelf import Shelf
from bookshelf.book import Book
from bookshelf.article import Article
from zope.interface import Interface

class BookShelf(grok.Application, grok.Container):
    def __init__(self):
        super(BookShelf, self).__init__()
        self['shelf'] = Shelf()

class Index(grok.View):
    pass

class BookIndexes(grok.Indexes):
    grok.site(BookShelf)
    grok.context(Book)

    title = index.Text()

#class ArticleIndexes(grok.Indexes):
#    grok.site(BookShelf)
#    grok.context(Article)
#
#    title = index.Text()

class Master(grok.View):
    """ The master page template macro """
    grok.context(Interface)
