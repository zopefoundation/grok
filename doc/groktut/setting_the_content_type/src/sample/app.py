import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def render(self):
        self.response.setHeader('Content-Type',
                                'text/xml; charset=UTF-8')
        return "<doc>Some XML</doc>"
