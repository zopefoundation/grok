import sys

from zope.interface import implements
from zope.interface.interfaces import IMethod

from zope.app.catalog.field import FieldIndex
from zope.app.catalog.text import TextIndex

from grok.error import GrokError
from grok.directive import frame_is_class
from grok.interfaces import IIndexDefinition

class IndexDefinition(object):
    implements(IIndexDefinition)
    
    def __init__(self, *args, **kw):
        frame = sys._getframe(1)
        if not frame_is_class(frame):
            raise GrokError('Index definition can only be used on a class.')
        # store any extra parameters to pass to index later
        self._args = args
        self._kw = kw

    def setup(self, catalog, name, context):
        raise NotImplementedError

class Field(IndexDefinition):
    def setup(self, catalog, name, context):
        call = IMethod.providedBy(context[name])
        catalog[name] = FieldIndex(name, context, *self._args, **self._kw)

class Text(IndexDefinition):
    def setup(self, catalog, name, context):
        call = IMethod.providedBy(context[name]) 
        catalog[name] = TextIndex(name, context, call, *self._args, **self._kw)
