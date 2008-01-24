import grok
from datetime import datetime

class Sample(grok.Application, grok.Container):
    pass

class Index(grok.View):    
    def current_datetime(self):
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M')
