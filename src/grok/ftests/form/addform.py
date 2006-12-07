"""
A grok.AddForm is a special grok.View that renders an add form.

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

"""
import grok
from zope import schema

class Zoo(grok.Container):
    pass

class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size")

    def __init__(self, name, size):
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
        self.context['manfred'] = Mammoth(data['name'], data['size'])
        self.redirect(self.url(self.context['manfred']))

