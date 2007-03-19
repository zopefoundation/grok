import grok

class testproj(grok.Application, grok.Container):
    pass

class Index(grok.View):
    pass # see app_templates/index.pt