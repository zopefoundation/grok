import grok
from book import Book
#from article import Article
from zope.app.container.contained import NameChooser as BaseNameChooser
from zope.app.container.interfaces import INameChooser
from zope.interface import implements
from operator import attrgetter

from zope.app.catalog.interfaces import ICatalog
from zope.component import getUtility

class Shelf(grok.Container):
    """
    A shelf is a container for books and articles, used for containment and searching.
    """

class Index(grok.View):
    
    def update(self, query=None):
        if not query:
            # XXX: if the query is empty, return all books; this should change
            # to some limited default search criteria or none at all
            results = self.context.values()
            self.results_title = 'All items'
        else:
            catalog = getUtility(ICatalog)
            results = catalog.searchResults(title=query)
            # Note: to sort the results, we must cast the result iterable
            # to a list, which can be very expensive
            results = list(results)
            if len(results) == 0:
                qty = u'No i'
                s = u's'
            elif len(results) == 1:
                qty = u'I'
                s = u''
            else:
                qty = u'%s i' % len(results)
                s = u's'
            self.results_title = u'%stem%s matching "%s"' % (qty, s, query)

        self.results = sorted(results, key=attrgetter('title'))


class AddBook(grok.AddForm):

    form_fields = grok.AutoFields(Book)

    @grok.action('Add book')
    def add(self, **data):
        shelf = self.context
        book = Book()
        self.applyData(book, **data)
        name = INameChooser(shelf).chooseName(data.get('title'), book)
        shelf[name] = book
        self.redirect(self.url(shelf))

#class AddArticle(grok.AddForm):

#    form_fields = grok.AutoFields(Article)
#
#    @grok.action('Add article')
#    def add(self, **data):
#        shelf = self.context
#        article = Article()
#        self.applyData(article, **data)
#        name = INameChooser(shelf).chooseName(data.get('title'), article)
#        shelf[name] = article
#        self.redirect(self.url(shelf))

class NameChooser(grok.Adapter, BaseNameChooser):
    implements(INameChooser)

    def nextId(self,fmt='%s'):
        """ Binary search to quickly find an unused numbered key. The 
            algorithm generates a key right after the largest numbered 
            key or in some unused lower numbered slot found by the second 
            loop. If keys are later deleted in random order, some of the 
            resulting slots will be reused and some will not.
        """
        i = 1
        while fmt%i in self.context:
            i *= 2
        blank = i
        full = i//2
        while blank > (full+1):
            i = (blank+full)//2
            if fmt%i in self.context:
                full = i
            else:
                blank = i
        return fmt%blank

    def chooseName(self, name, object):
        name = name or self.nextId('k%04d')
        # Note: potential concurrency problems of nextId are (hopefully)
        # handled by calling the super.NameChooser
        return super(NameChooser, self).chooseName(name, object)

class ShelfRPC(grok.XMLRPC):
    """ShelfRPC is a XMLRPC interface to the shelf model.
    """

    def list(self):
        return list(self.context.keys())

    def addBook(self, book_dict):
        shelf = self.context
        book = Book(**book_dict)
        name = INameChooser(shelf).chooseName(book_dict.get('title'), book)
        shelf[name] = book
        return name
