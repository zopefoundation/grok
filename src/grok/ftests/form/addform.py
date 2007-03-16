"""
We can use grok.Form to render an add form for objects:

  >>> import grok
  >>> from grok.ftests.form.addform import Zoo, Mammoth
  >>> grok.grok('grok.ftests.form.addform')
  >>> getRootFolder()["zoo"] = Zoo()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

  >>> browser.open("http://localhost/zoo/@@addmammoth")
  >>> browser.getControl(name="form.name").value = "Manfred the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really big"
  >>> browser.getControl("Add entry").click()
  >>> print browser.contents
  Hi, my name is Manfred the Mammoth, and I\'m "Really big"

  >>> browser.open("http://localhost/zoo/@@addmammothapplychanges")
  >>> browser.getControl(name="form.name").value = "Ellie the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really small"
  >>> browser.getControl("Add entry").click()
  >>> print browser.contents
  Hi, my name is Ellie the Mammoth, and I\'m "Really small"

"""
import grok
from zope import schema

class Zoo(grok.Container):
    pass

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size")

    def __init__(self, name='', size=''):
        self.name = name
        self.size = size

class Index(grok.View):
    grok.context(Mammoth)
    def render(self):
        return 'Hi, my name is %s, and I\'m "%s"' % (self.context.name,
                                                     self.context.size)

class AddMammoth(grok.AddForm):
    grok.context(Zoo)

    form_fields = grok.AutoFields(Mammoth)

    @grok.action('Add entry')
    def add(self, **data):
        # pass data into Mammoth constructor
        self.context['manfred'] = manfred = Mammoth(**data)
        self.redirect(self.url(manfred))

class AddMammothApplyChanges(AddMammoth):

    @grok.action('Add entry')
    def add(self, **data):
        # instantiate Mammoth and then use self.apply_changes()
        self.context['ellie'] = ellie = Mammoth()
        self.apply_changes(ellie, **data)
        self.redirect(self.url(ellie))
