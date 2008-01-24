import grok
  
class Sample(grok.Application, grok.Container):
    pass

class Another(grok.Application, grok.Model):
    pass

class SampleIndex(grok.View):
    grok.context(Sample)
    grok.name('index')
    
class AnotherIndex(grok.View):
    grok.context(Another)
    grok.name('index')
