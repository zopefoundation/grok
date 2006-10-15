import grok

class CalcApp(grok.App):
    """calculator model that's also a site

    whenever you create one of those, all local utilities will be
    registered with it automatically.
    """

class Calculator(grok.Utility):
    grok.implements(ICalculator)  # if this is not specified, it breaks
    grok.name('')  # this is actually the default
    grok.register(site=CalcApp)  # register this only in calculator app sites

