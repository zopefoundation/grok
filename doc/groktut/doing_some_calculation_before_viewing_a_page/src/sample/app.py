import grok

class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self):
        self.alpha = 2 ** 8

