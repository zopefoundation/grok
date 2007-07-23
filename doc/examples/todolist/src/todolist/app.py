import grok
from zope import schema
from todolist.todoitem import TodoItem

class TodoList(grok.Application, grok.Container):
    pass

class Index(grok.View):
    pass # see app_templates/index.pt

class AddTodoItem(grok.AddForm):
    
    form_fields = grok.Fields(
        title = schema.TextLine(title=u'Title')
        )
        
    @grok.action('Add')
    def add(self,title):
        name = title.lower().replace(' ','-')
        item = TodoItem(title)
        self.context[name] = item
        self.redirect(self.url(item))
        
class DeleteItem(grok.View):

    def render(self):
        name = self.request.form.get('name')
        if name is not None:
            del self.context[name]
        self.redirect(self.url(self.context))

        