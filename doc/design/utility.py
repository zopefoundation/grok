import grok

class Calculator(grok.GlobalUtility):
    grok.implements(ICalculator)  # if this is not specified, it breaks
    grok.name('')  # this is actually the default
    grok.provides(ICalculator) # this is actually the default

grok.global_utility(factory, provides=IFace, name=u'')

class Calculator(grok.LocalUtility):
    grok.utility_provides(ICalculator)

class Anything(grok.Model):
    pass

class NonPersistent(object):
    pass

class SpecialAnything(Anything):
    pass

class Foo(grok.Model, grok.Site):    
    grok.local_utility(Anything, hide=False, name_in_container='foo',
                       persistent=None)
    grok.local_adapter()
    grok.local_view()

class Foo2(Foo):
    grok.local_utility(SpecialAnything)

    
