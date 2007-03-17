import grok

class Sample(grok.Application, grok.Container):
    def information(self):
        return "This is important information!"

class Index(grok.View):
    def reversed_information(self):
        return ''.join(reversed(self.context.information()))
