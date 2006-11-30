"""
A grok.Model may implement one or more interfaces that are schemas:

  >>> grok.grok(__name__)
  >>> manfred = Mammoth()

A grok.EditForm is a special grok.View that renders an edit form.

We need to set up the default formlib template first, because even though we
don't use the formlib NamedTemplates directly they need to be present to create
a formlib form.

  >>> from zope import component
  >>> from zope.formlib import form
  >>> component.provideAdapter(form.default_page_template, name='default')

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
