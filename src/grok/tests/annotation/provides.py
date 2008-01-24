"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)

If an annotation class implements more than one interface, it has to
declare which one it should be registered for using ``grok.provides``.

  >>> manfred = Mammoth()
  >>> ann = IOneInterface(manfred)

It can then be looked up only using that one interface:

  >>> IAnotherOne(manfred)
  Traceback (most recent call last):
  TypeError: ('Could not adapt', <grok.tests.annotation.provides.Mammoth object at ...>, <InterfaceClass grok.tests.annotation.provides.IAnotherOne>)


"""

import grok
from zope import interface
from BTrees.OOBTree import OOTreeSet

class Mammoth(grok.Model):
    pass

class IOneInterface(interface.Interface):
    pass

class IAnotherOne(interface.Interface):
    pass

class MammothAnnotation(grok.Annotation):
    grok.implements(IOneInterface, IAnotherOne)
    grok.provides(IOneInterface)
