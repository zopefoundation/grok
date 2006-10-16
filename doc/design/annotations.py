import grok

class Article(grok.Model):
    pass

class Comments(grok.Annotation):
    grok.context(Article)  # this is actually the default
    grok.implements(IComments)

    def __init__(self): 
        # XXX need super?!?
        self.comments = OOTreeSet()

    def addComment(self, text):
        self.comments.insert(text)

    def getComments(self):
        return list(self.comments)
