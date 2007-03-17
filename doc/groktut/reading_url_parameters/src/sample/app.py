import grok

class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self, value1, value2):
        self.sum = int(value1) + int(value2)
