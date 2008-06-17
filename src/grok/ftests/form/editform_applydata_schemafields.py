"""
A grok.EditForm uses applyData in update mode to save the form data on
the object.  Update mode means that only those fields are changed on
the object that need to be changed.

This is essentially the same narrative as 'editform_applydata'. Here we
test the whole procedure on fields on the interface implemented by the
model class:

  >>> getRootFolder()["manfred"] = mammoth = Mammoth()
  >>> mammoth.name = 'Manfred the Mammoth'
  >>> mammoth.size = 'Really big'

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

If we don't change any of the fields, there will no object modified
event and applyData will report no changes:

  >>> browser.open("http://localhost/manfred/@@edit")
  >>> browser.getControl("Apply").click()
  >>> 'No changes' in browser.contents
  True

If we change one field, only that attribute will be changed.  The
object modified event also reflects that:

  >>> browser.getControl(name="form.name").value = "Manfred the Big Mammoth"
  >>> browser.getControl("Apply").click()
  An IObjectModifiedEvent was sent for a mammoth with the following changes:
  name
  >>> 'Updated' in browser.contents
  True

Let's change the other field:

  >>> browser.getControl(name="form.size").value = "Enormously big"
  >>> browser.getControl("Apply").click()
  An IObjectModifiedEvent was sent for a mammoth with the following changes:
  size
  >>> 'Updated' in browser.contents
  True

And finally let's change both fields:

  >>> browser.getControl(name="form.name").value = "Manfred the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really big"
  >>> browser.getControl("Apply").click()
  An IObjectModifiedEvent was sent for a mammoth with the following changes:
  name, size
  >>> 'Updated' in browser.contents
  True

"""
import grok
from zope import schema
from zope.interface import Interface, implements

class IMammoth(Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size", default=u"Quite normal")

class Mammoth(grok.Model):
    implements(IMammoth)
    
class Edit(grok.EditForm):
    pass

@grok.subscribe(Mammoth, grok.IObjectModifiedEvent)
def notify_change_event(mammoth, event):
    print ("An IObjectModifiedEvent was sent for a mammoth with the "
           "following changes:")
    for descr in event.descriptions:
        print ", ".join(descr.attributes)
