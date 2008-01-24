"""
  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.annotation.attribute import AttributeAnnotations
  >>> component.provideAdapter(AttributeAnnotations)

We can adapt a model to an annotation interface and obtain a
persistent annotation storage:

  >>> manfred = Mammoth()
  >>> branding = IBranding(manfred)
  >>> branding.addBrand('mine')
  >>> branding.addBrand('yours')

Regetting the adapter will yield the same annotation storage:

  >>> brands = IBranding(manfred).getBrands()
  >>> brands.sort()
  >>> brands
  ['mine', 'yours']

"""

import grok
from zope import interface
from BTrees.OOBTree import OOTreeSet

class Mammoth(grok.Model):
    pass

class IBranding(interface.Interface):

    def addBrand(brand):
        """Brand an animal with ``brand``, a string."""

    def getBrands():
        """Return a list of brands."""

class Branding(grok.Annotation):
    grok.implements(IBranding)

    def __init__(self): 
        self._brands = OOTreeSet()

    def addBrand(self, brand):
        self._brands.insert(brand)

    def getBrands(self):
        return list(self._brands)
