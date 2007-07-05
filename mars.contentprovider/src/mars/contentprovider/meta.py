import zope.component
from zope.publisher.interfaces.browser import IBrowserView
from zope.contentprovider.interfaces import IContentProvider

import mars.contentprovider
from mars.view.meta import ViewGrokkerBase

class ContentProviderGrokker(ViewGrokkerBase):
    component_class = mars.contentprovider.ContentProvider
    provides = IContentProvider
    
    def register(self, factory, module_info):

        zope.component.provideAdapter(factory,
                                 adapts=(self.view_context, self.view_layer, IBrowserView),
                                 provides=self.provides,
                                 name=self.view_name)

