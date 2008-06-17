import grok

class Sample(grok.Application, grok.Container):
    text = 'default text'

class Index(grok.View):
    pass

class Edit(grok.View):
    def update(self, text=None):
        if text is None:
            return
        self.context.text = text
        self.redirect(self.url('index'))
