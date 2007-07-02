import martian
import grok
import zope.component
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserRequest,
                                               IBrowserSkinType)
from martian import util
import megrok.layer
from megrok.layer.components import ILayer

class ILayerGrokker(martian.ClassGrokker):
    component_class = ILayer


class SkinGrokker(martian.ClassGrokker):
    component_class = megrok.layer.Skin

    def grok(self, name, factory, context, module_info, templates):
        layer = util.class_annotation(factory, 'megrok.layer.layer',
                                    None) or module_info.getAnnotation('megrok.layer.layer',
                                    None) or IBrowserRequest
        name = grok.util.class_annotation(factory, 'grok.name', factory.__name__.lower())
        zope.component.interface.provideInterface(name, layer, IBrowserSkinType)

        return True

