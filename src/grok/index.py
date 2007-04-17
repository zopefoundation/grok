import sys

from zope.interface import implements
from zope.interface.interfaces import IMethod, IInterface

from zope.app.catalog.field import FieldIndex
from zope.app.catalog.text import TextIndex

from grok.error import GrokError
from grok.directive import frame_is_class
from grok.interfaces import IIndexDefinition

class IndexDefinition(object):
    implements(IIndexDefinition)

    index_class = None
    
    def __init__(self, *args, **kw):
        frame = sys._getframe(1)
        if not frame_is_class(frame):
            raise GrokError('Index definition can only be used on a class.')
        # store any extra parameters to pass to index later
        self._args = args
        self._kw = kw

    def setup(self, catalog, name, context):
        if IInterface.providedBy(context):
            call = IMethod.providedBy(context[name])
        else:
            call = callable(getattr(context, name, None))
            context = None # no interface lookup
        catalog[name] = self.index_class(field_name=name,
                                         interface=context,
                                         field_callable=call,
                                         *self._args, **self._kw)

class Field(IndexDefinition):
    index_class = FieldIndex

class Text(IndexDefinition):
    index_class = TextIndex
