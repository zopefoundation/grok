import sys

from zope.interface import implements
from zope.interface.interfaces import IMethod, IInterface

from zope.app.catalog.field import FieldIndex
from zope.app.catalog.text import TextIndex
from zc.catalog.catalogindex import SetIndex

from martian.error import GrokError, GrokImportError
from martian.util import frame_is_class

from grok.interfaces import IIndexDefinition

class IndexDefinition(object):
    implements(IIndexDefinition)

    index_class = None

    def __init__(self, *args, **kw):
        frame = sys._getframe(1)
        if not frame_is_class(frame):
            raise GrokImportError(
                "%r can only be instantiated on class level." % self.__class__)
        # store any extra parameters to pass to index later
        self._args = args
        self._attribute = kw.pop('attribute', None)
        self._kw = kw

    def setup(self, catalog, name, context, module_info):
        if self._attribute is not None:
            field_name = self._attribute
        else:
            field_name = name

        if IInterface.providedBy(context):
            try:
                method = context[field_name]
            except KeyError:
                raise GrokError("grok.Indexes in %r refers to an attribute or "
                                "method %r on interface %r, but this does not "
                                "exist." % (module_info.getModule(),
                                            field_name, context), None)
            call = IMethod.providedBy(method)
        else:
            call = callable(getattr(context, field_name, None))
            context = None # no interface lookup
        catalog[name] = self.index_class(field_name=field_name,
                                         interface=context,
                                         field_callable=call,
                                         *self._args, **self._kw)

class Field(IndexDefinition):
    index_class = FieldIndex

class Text(IndexDefinition):
    index_class = TextIndex

class Set(IndexDefinition):
    index_class = SetIndex
