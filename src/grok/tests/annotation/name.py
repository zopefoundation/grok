"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)

If an annotation class doesn't specify anything else, its dotted name
will be used as an annotation key:

  >>> manfred = Mammoth()
  >>> ann = IImplicitName(manfred)

  >>> from zope.annotation.interfaces import IAnnotations
  >>> 'grok.tests.annotation.name.ImplicitName' in IAnnotations(manfred)
  True

Of course, annotation classes can explicity specify the name of the
annotation key that they will be stored under.  That's useful if you
want a meaningful key that's accessible from other applications and if
you want to be able to move the class around during refactorings (then
the dotted name will obviously change)

  >>> ann = IExplicitName(manfred)
  >>> 'grok.tests.annotation.name.ExplicitName' in IAnnotations(manfred)
  False
  >>> 'mammoth.branding' in IAnnotations(manfred)
  True

"""

import grok
from zope import interface
from BTrees.OOBTree import OOTreeSet

class Mammoth(grok.Model):
    pass

class IExplicitName(interface.Interface):
    pass

class IImplicitName(interface.Interface):
    pass

class ExplicitName(grok.Annotation):
    grok.implements(IExplicitName)
    grok.name('mammoth.branding')

class ImplicitName(grok.Annotation):
    grok.implements(IImplicitName)
