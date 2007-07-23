import grok
from zope import schema

class TodoItem(grok.Model):
    
    def __init__(self, title):
        self.title = title
        
#XXX needed to add this
class Index(grok.View):
    pass
    
class Edit(grok.EditForm):
    
    form_fields = grok.Fields(
        #XXX why repeat this?
        title = schema.TextLine(title=u'Title')
        )
    
    @grok.action('Save')
    def save(self, title):
        self.applyChanges(self.context,title=title)
        self.redirect(self.url(self.context))

