"""
You can subscribe to events using the @grok.subscribe decorator:

  >>> grok.grok(__name__)
  >>> manfred = Mammoth('Manfred')
  >>> grok.notify(grok.ObjectCreatedEvent(manfred))
  >>> mammoths
  ['Manfred']

"""
import grok

class Mammoth(object):
    def __init__(self, name):
        self.name = name

mammoths = []

@grok.subscribe(Mammoth, grok.IObjectCreatedEvent)
def mammothAdded(mammoth, event):
    mammoths.append(mammoth.name)
