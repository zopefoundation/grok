import zope.component
import grok.interfaces
from zope.app.folder.interfaces import IRootFolder

grok.context(IRootFolder)
grok.define_permission('grok.ManageApplications')

class Index(grok.View):
    grok.name('index.html') # the root folder isn't a grok.Model
    grok.require('grok.ManageApplications')

    def update(self):
        apps = zope.component.getAllUtilitiesRegisteredFor(
            grok.interfaces.IApplication)
        self.applications = ("%s.%s" % (x.__module__, x.__name__)
                             for x in apps)

class Macros(grok.View):
    """Only to contain the standard macros."""
    grok.context(IRootFolder)
    pass

class Add(grok.View):
    grok.require('grok.ManageApplications')

    def render(self, application, name):
        if name is None or name == "":
            self.redirect(self.url(self.context))
            return
        app = zope.component.getUtility(grok.interfaces.IApplication,
                                        name=application)
        self.context[name] = app()
        self.redirect(self.url(self.context))

class Delete(grok.View):
    grok.require('grok.ManageApplications')

    def render(self, items=None):
        if items is None:
            self.redirect(self.url(self.context))
            return
        if not isinstance(items, list):
            items = [items]
        for name in items:
            del self.context[name]
        self.redirect(self.url(self.context))

