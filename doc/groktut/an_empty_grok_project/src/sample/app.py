import grok

class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    pass # see app_templates/index.pt
