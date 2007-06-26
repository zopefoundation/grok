from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from calc import Calculator
import grok

@grok.subscriber(Calculator, IObjectModifiedEvent)
def calculatorChanged(calc, event):
    pass


# perhaps alias zope.event.notify to grok.notify???

