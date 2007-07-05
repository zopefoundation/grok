import zope.interface
from zope.component.interfaces import ComponentLookupError
from zope.publisher.browser import BrowserView
from zope.publisher.publish import mapply
from zope.viewlet.interfaces import IViewlet, IViewletManager

from z3c.viewlet.manager import WeightOrderedViewletManager

from martian import util

from mars.view.components import TemplateViewBase

class Viewlet(TemplateViewBase, BrowserView):
    zope.interface.implements(IViewlet)

    def __init__(self, context, request, view, manager):
        self.__parent__ = self.view = view
        self.context = context
        self.request = request
        self.manager = manager

class ViewletManager(WeightOrderedViewletManager, TemplateViewBase):
    zope.interface.implements(IViewletManager)

    def __init__(self, context, request, view):
        self.__updated = False
        self.__parent__ = self.view = view
        self.context = context
        self.request = request

    def render(self):
        """Allows template rendering before falling back to the viewlets"""
        template = getattr(self, 'template', None)
        if template is not None:
            return template(self)
        else:
            try:
                template = zope.component.getMultiAdapter(
                    (self, self.request), self._template_interface, 
                    name=self._template_name)
                return template(self)
            except ComponentLookupError:
                return u'\n'.join([viewlet.render() for viewlet in self.viewlets])

    def update_manager(self):
        super(ViewletManager, self).update()


    def filter(self, viewlets):
        """Sort out all content providers

        ``viewlets`` is a list of tuples of the form (name, viewlet).
        """
# this is the original for z.v.manager.py but I would get ForbiddenAttribute: ('render'
# for the viewlets, I need to go a step and create security checkers on viewlets
# as on Views
        # Only return viewlets accessible to the principal
        #import zope.security
        #return [(name, viewlet) for name, viewlet in viewlets
        #                        if zope.security.canAccess(viewlet, 'render')]
        return [(name, viewlet) for name, viewlet in viewlets]
