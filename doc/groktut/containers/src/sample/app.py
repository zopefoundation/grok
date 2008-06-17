import grok

class Sample(grok.Application, grok.Container):
    pass

class Entry(grok.Model):
    def __init__(self, text):
        self.text = text

class SampleIndex(grok.View):
    grok.context(Sample)
    grok.name('index')

    def update(self, name=None, text=None):
        if name is None or text is None:
            return
        self.context[name] = Entry(text)

class EntryIndex(grok.View):
    grok.context(Entry)
    grok.name('index')
