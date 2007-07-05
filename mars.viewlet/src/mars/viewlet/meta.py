import zope.component
from zope.publisher.interfaces.browser import IBrowserView

from zope.viewlet.interfaces import IViewlet, IViewletManager

from martian import util

import mars.viewlet
from mars.view.meta import ViewGrokkerBase

class ViewletManagerGrokker(ViewGrokkerBase):
    component_class = mars.viewlet.ViewletManager
    provides = IViewletManager
    
    def register(self, factory, module_info):

#        print '\nname:', self.view_name,'context:', self.view_context,'factory:', factory,\
#              'layer:', self.view_layer, 'provides', self.provides, '\n'
        zope.component.provideAdapter(factory,
                     adapts=(self.view_context, self.view_layer, IBrowserView),
                     provides=self.provides,
                     name=self.view_name)


class ViewletGrokker(ViewGrokkerBase):
    component_class = mars.viewlet.Viewlet

    def register(self, factory, module_info):

        manager = util.class_annotation(factory, 'mars.viewlet.manager',
                       None) or module_info.getAnnotation('mars.viewlet.manager',
                       None) or IViewletManager # IViewletManager?

        view = util.class_annotation(factory, 'mars.viewlet.view',
                       None) or IBrowserView
#        print '\nname:', self.view_name,'context:', self.view_context,'factory:', factory,\
#              'layer:', self.view_layer, 'manager', manager, 'view: ', view,'\n'
        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer, 
                                         view, manager),
                                 provides=IViewlet,
                                 name=self.view_name)


