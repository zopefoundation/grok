import zope.component
from zope.publisher.interfaces.browser import IBrowserView
from zope.contentprovider.interfaces import IContentProvider

import mars.contentprovider
from mars.view.meta import ViewGrokkerBase

class ContentProviderGrokker(ViewGrokkerBase):
    component_class = mars.contentprovider.ContentProvider
    provides = IContentProvider
    
    def register(self, factory, module_info):

#        print '\nname:', self.view_name,'context:', self.view_context,'factory:', factory,\
#              'layer:', self.view_layer, 'provides', self.provides, '\n'
        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer, IBrowserView),
                                 provides=self.provides,
                                 name=self.view_name)

