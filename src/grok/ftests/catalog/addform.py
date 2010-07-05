"""
Thanks to Zope's event system, newly added objects are automatically
catalogued, should a catalog be present.

  >>> getRootFolder()["zoo"] = Zoo()

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

Let's demonstrate that an object that has not been added to a
container yet can still be modified using a form's applyData method.
Event though this method triggers an IObjectModifiedEvent, the catalog
won't be bothered by this.  It will start the indexation when the
object has been *added* to a container, not before.

  >>> browser.open("http://localhost/zoo/@@addmammoth")
  >>> browser.getControl(name="form.name").value = "Ellie the Mammoth"
  >>> browser.getControl(name="form.size").value = "Really small"
  >>> browser.getControl("Add entry").click()

  >>> browser.open("http://localhost/zoo/ellie")
  >>> print browser.contents
  Hi, my name is Ellie the Mammoth, and I\'m "Really small"

Let's ensure the catalog has actually indexed the object with the
right value:

  >>> browser.open("http://localhost/zoo/search")
  >>> print browser.contents
  We found Ellie!

"""
import grok
from zope import schema, interface, component
from zope.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope.catalog.catalog import Catalog
from zope.catalog.interfaces import ICatalog
from zope.catalog.field import FieldIndex

def setup_catalog(catalog):
    catalog['name'] = FieldIndex('name', IMammoth)

class Zoo(grok.Site, grok.Container):
    grok.local_utility(IntIds, provides=IIntIds)
    grok.local_utility(Catalog, provides=ICatalog, setup=setup_catalog)

class IMammoth(interface.Interface):
    name = schema.TextLine(title=u"Name")
    size = schema.TextLine(title=u"Size")

class Mammoth(grok.Model):
    grok.implements(IMammoth)

class Index(grok.View):
    grok.context(Mammoth)

    def render(self):
        return 'Hi, my name is %s, and I\'m "%s"' % (self.context.name,
                                                     self.context.size)

class Search(grok.View):
    grok.context(Zoo)

    def render(self):
        catalog = component.getUtility(ICatalog)
        query = ('Ellie the Mammoth', 'Ellie the Mammoth')
        results = catalog.searchResults(name=query)
        if len(list(results)) == 1:
            return 'We found Ellie!'
        return "Couldn't find Ellie."

class AddMammoth(grok.AddForm):
    grok.context(Zoo)

    form_fields = grok.AutoFields(IMammoth)

    @grok.action('Add entry')
    def add(self, **data):
        # First apply the form data, thus triggering an
        # IObjectModifiedEvent.  This test case demonstrates that this
        # isn't a problem.
        ellie = Mammoth()
        self.applyData(ellie, **data)
        self.context['ellie'] = ellie
