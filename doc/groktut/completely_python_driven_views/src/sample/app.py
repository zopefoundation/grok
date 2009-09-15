import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Index(grok.CodeView):
    def render(self):
        return "ME GROK NO TEMPLATE"
