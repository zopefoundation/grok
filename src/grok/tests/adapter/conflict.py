"""
Registering two adapters for the same target interface should provoke
a conflict, even if the interface is guessed (instead of being
explicitly declared with grok.provides):

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  ConfigurationConflictError: Conflicting configuration actions
    For: ('adapter', <InterfaceClass grok.tests.adapter.conflict.ICave>, <InterfaceClass grok.tests.adapter.conflict.IDecoration>, '')

"""
import grok
from zope.interface import Interface

class ICave(Interface):
    pass

class IDecoration(Interface):
    pass

class ICaveCleaning(Interface):
    pass

class Cave(object):
    grok.implements(ICave)


class ImplicitProvides(grok.Adapter):
    """Here the provided interface is guessed because the class only
    implements one interface."""
    grok.context(ICave)
    grok.implements(IDecoration)

class ExplicitProvides(grok.Adapter):
    """Here the provided interface is specific explicitly."""
    grok.context(ICave)
    grok.implements(IDecoration, ICaveCleaning)
    grok.provides(IDecoration)
