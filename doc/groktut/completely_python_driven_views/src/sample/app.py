import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def render(self):
        return "ME GROK NO TEMPLATE"
