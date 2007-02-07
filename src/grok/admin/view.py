import zope.component
import grok.interfaces

from zope.app import zapi


class Admin(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def applications(self):
        apps = zope.component.getAllUtilitiesRegisteredFor(
            grok.interfaces.IApplication)
        return ["%s.%s" % (x.__module__, x.__name__)
                for x in apps]

    def add(self, application, name):
        app = zope.component.getUtility(grok.interfaces.IApplication,
                                        name=application)
        self.context[name] = app()
        self.request.response.redirect(zapi.absoluteURL(self.context,
                                                        self.request))
