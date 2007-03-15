"""
A grok.Model may implement one or more interfaces that are schemas:

  >>> grok.grok(__name__)
  >>> manfred = Mammoth()

A grok.EditForm is a special grok.View that renders an edit form.

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((manfred, request), name='edit')
  >>> len(view.form_fields)
  2
  >>> [w.__name__ for w in view.form_fields]
  ['name', 'size']

When there are multiple schemas in play, we get all the fields:

  >>> view = component.getMultiAdapter((Manfred(), request), name='edit2')
  >>> len(view.form_fields)
  3
  >>> [w.__name__ for w in view.form_fields]
  ['can_talk', 'name', 'size']

Schema fields and model level fields are combined:

  >>> view = component.getMultiAdapter(
  ...    (AnotherMammoth(), request), name='edit3')
  >>> len(view.form_fields)
  3
  >>> [w.__name__ for w in view.form_fields]
  ['can_talk', 'name', 'size']

If the context is an interface instead of a model directly, the fields
will be retrieved from that interface, and that interface only:

  >>> view = component.getMultiAdapter(
  ...   (YetAnotherMammoth(), request), name='edit4')
  >>> len(view.form_fields)
  2
  >>> [w.__name__ for w in view.form_fields]
  ['alpha', 'beta']

"""
import grok
from zope import interface, schema

class IMammoth(interface.Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    interface.implements(IMammoth)

class Edit(grok.EditForm):
    grok.context(Mammoth)

class IMovieCharacter(interface.Interface):
    can_talk = schema.Bool(title=u'Can talk', default=False)

class Manfred(Mammoth):
    interface.implements(IMovieCharacter)

class Edit2(grok.EditForm):
    grok.context(Manfred)
    
class AnotherMammoth(Mammoth):
    class fields:
        can_talk = schema.Bool(title=u'Can talk', default=False)

class Edit3(grok.EditForm):
    grok.context(AnotherMammoth)

class IYetAnotherMammoth(interface.Interface):
    alpha = schema.TextLine(title=u'alpha')
    beta = schema.TextLine(title=u'beta')

class YetAnotherMammoth(grok.Model):
    interface.implements(IYetAnotherMammoth)

class Edit4(grok.EditForm):
    grok.context(IYetAnotherMammoth)
