#############################################################################
#
# Copyright (c) 2007-2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok index definitions
"""
import sys

from zope.interface import implements
from zope.interface.interfaces import IMethod, IInterface

from zope.catalog.field import FieldIndex
from zope.catalog.text import TextIndex
from zc.catalog.catalogindex import SetIndex, ValueIndex

from martian.error import GrokError, GrokImportError
from martian.util import frame_is_class

from grok.interfaces import IIndexDefinition


class IndexDefinition(object):
    """The definition of a particular index in a :data:`grok.Indexes`
    class.

    This base class defines the actual behavior of
    :class:`grok.index.Field` and the other kinds of attribute index
    that Grok supports.  Upon our instantiation, we save every
    parameter that we were passed; later, if an index actually needs
    to be created (which is typically at the moment when a new
    :class:`grok.Application` object is added to the Zope Database),
    then our :meth:`setup()` method gets called.

    The only parameter that is actually significant to us is `attribute`
    which (optionally) defines the attribute we should index.  All other
    parameters are simply passed along to the Zope index we create,
    which interprets them as configuration details of its own.

    Note that, since index creation (and thus a call to our
    :meth:`setup()` method) currently occurs only during the creation
    of a new Grok `Application` object in the Zope Database, the
    presence of this declaration in Grok application code is nearly
    always a no-op.

    """
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
        # If the user supplied attribute= when instantiating us, we
        # allow that value to override the attribute name under which we
        # are actually stored inside of the `grok.Indexes` instance.
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
            context = None  # no interface lookup
        catalog[name] = self.index_class(field_name=field_name,
                                         interface=context,
                                         field_callable=call,
                                         *self._args, **self._kw)


class Field(IndexDefinition):
    """A :class:`grok.Indexes` index that matches against an entire field."""
    index_class = FieldIndex


class Text(IndexDefinition):
    """A :class:`grok.Indexes` index supporting full-text searches of a
    field."""
    index_class = TextIndex


class Set(IndexDefinition):
    """A :class:`grok.Indexes` index supporting keyword searches of a field."""
    index_class = SetIndex


class Value(IndexDefinition):
    """A :class:`grok.Indexes` index similar to, but more flexible than
    :class:`grok.Field` index.

    The index allows searches for documents that contain any of a set of
    values; between a set of values; any (non-None) values; and any empty
    values.
    """
    index_class = ValueIndex
