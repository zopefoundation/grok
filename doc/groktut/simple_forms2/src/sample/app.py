import grok

class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self, value1=None, value2=None):
        try:
            value1 = int(value1)
            value2 = int(value2)
        except (TypeError, ValueError):
            self.sum = "No sum"
            return
        self.sum = value1 + value2
