import grok
from zope import interface

class IDummy(interface.Interface):
    pass

@grok.adapter()
@grok.implementer(IDummy)
def decorator_called_with_no_arguments(cave):
    pass
