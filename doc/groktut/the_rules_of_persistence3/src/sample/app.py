import grok

class Sample(grok.Application, grok.Container):
    def __init__(self):
        super(Sample, self).__init__()
        self.list = []

    def addText(self, text):
        self.list.append(text)
        self._p_changed = True
        
class Index(grok.View):
    pass

class Edit(grok.View):
    def update(self, text=None):
        if text is None:
            return
        self.context.addText(text)
        self.redirect(self.url('index'))
