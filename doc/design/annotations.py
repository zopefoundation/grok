import grok
from zope import interface
from BTrees.OOBTree import OOTreeSet

class Article(grok.Model):
    pass

class IComments(interface.Interface):

    def addComment(text):
        pass

    def getComments():
        pass

class Comments(grok.Annotation):
    grok.context(Article)  # this is actually the default
    grok.implements(IComments)
    grok.name('annotations.Comments')  # this is actually the default

    def __init__(self): 
        self.comments = OOTreeSet()

    def addComment(self, text):
        self.comments.insert(text)

    def getComments(self):
        return list(self.comments)
