import grok

class Sample(grok.Application, grok.Container):
    def __init__(self):
        super(Sample, self).__init__()
        self.list = []
    
class Index(grok.View):
    pass

class Edit(grok.View):
    def update(self, text=None):
        if text is None:
            return
        self.context.list.append(text)
        self.context._p_changed = True
        self.redirect(self.url('index'))
