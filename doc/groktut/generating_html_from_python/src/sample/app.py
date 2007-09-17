import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def some_html(self):
        return "<b>ME GROK BOLD</b>"

