"""
We can use grok.AddForm to render an add form for objects:

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

Instead of calling an object constructor with the form data, we can
also use the ``applyData`` method to store the data on the object.

  >>> browser.open("http://localhost/zoo/@@addmammothapplydata")
  >>> browser.getControl(name="form.name").value = "Ellie the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really small"
  >>> browser.getControl("Add entry").click()
  >>> print browser.contents
  Hi, my name is Ellie the Mammoth, and I\'m "Really small"

"""
import grok
from zope import schema
from zope.interface import Interface, implements

class Zoo(grok.Container):
    pass

class IMammoth(Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    implements(IMammoth)

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

class AddMammothApplyData(AddMammoth):

    @grok.action('Add entry')
    def add(self, **data):
        # instantiate Mammoth and then use self.applyData()
        self.context['ellie'] = ellie = Mammoth()
        self.applyData(ellie, **data)
        self.redirect(self.url(ellie))
