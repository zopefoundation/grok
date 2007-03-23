import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    grok.context(Sample)

class Bye(grok.View):
    grok.context(Sample)
    

