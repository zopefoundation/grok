"""
A grok.Model may implement a schema that inherits from another one:

  >>> grok.testing.grok(__name__)
  >>> manfred = Mammoth()

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

Without AutoFields, just a simple edit form:

  >>> view = component.getMultiAdapter((manfred, request), name='edit')
  >>> len(view.form_fields)
  3
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size', 'speciality']

With AutoFields:

  >>> view = component.getMultiAdapter((manfred, request), name='edit2')
  >>> len(view.form_fields)
  3
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size', 'speciality']

  >>> antimanfred = YetAnotherMammoth()
  >>> view = component.getMultiAdapter((antimanfred, request), name='edit3')
  >>> len(view.form_fields)
  3
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size', 'speciality']
"""
import grok
from zope import interface, schema

class IMammoth(interface.Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class ISpecialMammoth(IMammoth):
    speciality = schema.TextLine(title=u"Speciality")

class Mammoth(grok.Model):
    interface.implements(ISpecialMammoth)

class Edit(grok.EditForm):
    grok.context(Mammoth)

class Edit2(grok.EditForm):
    grok.context(Mammoth)

    form_fields = grok.AutoFields(Mammoth)

# situation where subclass implements something on top of base class
class AnotherMammoth(grok.Model):
    interface.implements(IMammoth)

class YetAnotherMammoth(AnotherMammoth):
    interface.implements(ISpecialMammoth)

class Edit3(grok.EditForm):
    grok.context(YetAnotherMammoth)
    
