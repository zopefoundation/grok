import grok
from zope.publisher.interfaces.browser import IBrowserRequest, IBrowserView
from zope.contentprovider.interfaces import IContentProvider
from calc import Calculator

class SingleAdapter(grok.Adapter):
    grok.context(Calculator)
    grok.adapts(Calculator)  # generally allowed, but not in this case, because there's already grok.context
    grok.implements(ISomething)  # if this is not specified, app breaks
    grok.provides(ISomething)  # if adapter implements more than one interface
    grok.name('')  # this is actually the default

    def something(self):
        """self.context is automatically provided"""
        return self.context.foo

class CalculatorContentProvider(grok.MultiAdapter)
    grok.adapts(Calculator, IBrowserRequest, IBrowserView)
    grok.implements(IContentProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    # ...
