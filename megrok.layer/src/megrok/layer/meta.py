import martian
import grok
import zope.component
from zope.publisher.interfaces.browser import (IDefaultBrowserLayer,
                                               IBrowserSkinType)
from martian import util
import megrok.layer

class ILayerGrokker(martian.ClassGrokker):
    component_class = megrok.layer.ILayer


class SkinGrokker(martian.ClassGrokker):
    component_class = megrok.layer.Skin

    def grok(self, name, factory, context, module_info, templates):
        layer = util.class_annotation(factory, 'megrok.layer.layer',
                                    None) or module_info.getAnnotation('megrok.layer.layer',
                                    None) or IDefaultBrowserLayer
        name = grok.util.class_annotation(factory, 'grok.name', factory.__name__.lower())
        zope.component.interface.provideInterface(name, layer, IBrowserSkinType)

        return True

