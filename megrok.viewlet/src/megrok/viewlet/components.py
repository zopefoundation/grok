import grok
from zope import component
from zope import interface

from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.browser import BrowserView
from zope.viewlet.interfaces import IViewlet
from zope.publisher.publish import mapply

from z3c.viewlet.manager import WeightOrderedViewletManager

from grok.components import ViewBase

class TemplateContentBase(object):
    """Mixin class to provide render method using given template"""

    template = None

    def render(self):
        """My concern here is that if subclass overrides this method then it
        will be the responsibility of the developer to call update()"""
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()


class ContentProvider(ViewBase, TemplateContentBase):

    def __init__(self, context, request, view):
        self.__parent__ = self.view = view
        self.context = context
        self.request = request
        self.static = component.queryAdapter(
            self.request,
            interface.Interface,
            name=self.module_info.package_dotted_name
            )        

class Viewlet(BrowserView, ViewBase, TemplateContentBase):
    """ A grok.View-like viewlet
    """
    interface.implements(IViewlet)

    def __init__(self, context, request, view, manager):
        #super(Viewlet, self).__init__(context, request)
        self.__parent__ = self.view = view
        self.context = context
        self.request = request
        self.manager = manager
        self.static = component.queryAdapter(
            self.request,
            interface.Interface,
            name=self.module_info.package_dotted_name
            )

# using z3c orderedviewletmanager
class ViewletManager(WeightOrderedViewletManager, ContentProvider):
    """  A grok.View-like ViewletManager
    """

    def __init__(self, context, request, view):
        self.__updated = False
        self.__parent__ = self.view = view
        self.context = context
        self.request = request
        self.static = component.queryAdapter(
            self.request,
            interface.Interface,
            name=self.module_info.package_dotted_name
            )

    def update(self):
        """Subclasses can override this method just like on regular
        grok.Views. It will be called before any viewlet processing
        happens."""
        pass

    def update_manager(self):
        """Update the manager, i.e. process the viewlets.

        On ViewletManagers, this is what the update() method is.
        In grok views, the update() method has a different meaning.
        That's why this method is called update_manager() in grok manager."""
        super(ViewletManager, self).update()

    def render(self):
        """First update the manager then the normal grok view update"""
        self.update_manager()
        #mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            return
        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()
        else:
            return u'\n'.join([viewlet.render() for viewlet in self.viewlets])

    def filter(self, viewlets):
        """Sort out all content providers

        ``viewlets`` is a list of tuples of the form (name, viewlet).
        """
# Only return viewlets accessible to the principal
# this is the original for z.v.manager.py but I would get ForbiddenAttribute: ('render'
# for the viewlets??
        #import zope.security
        #return [(name, viewlet) for name, viewlet in viewlets
        #                        if zope.security.canAccess(viewlet, 'render')]
        return [(name, viewlet) for name, viewlet in viewlets]


