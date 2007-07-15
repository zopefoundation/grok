import grok
from zope import interface, schema

class IArticle(interface.Interface):
    title = schema.TextLine(title=u"Title", required=True)

class Article(grok.Model):
    """
    A simple article with a title.

    >>> article = Article()
    >>> article.title
    >>> article.title = "How to use Catalog"
    >>> article.title
    'How to use Catalog'

    """
    interface.implements(IArticle)
    title = ''

    def __init__(self, title=None):
        super(Article, self).__init__()
        self.title = title

class Edit(grok.EditForm):
    pass

class Index(grok.DisplayForm):
    pass
