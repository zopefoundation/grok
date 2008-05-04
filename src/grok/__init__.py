##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Grok
"""

from zope.interface import implements
from zope.component import adapts
from zope.event import notify
from zope.app.component.hooks import getSite
from zope.lifecycleevent import (
    IObjectCreatedEvent, ObjectCreatedEvent,
    IObjectModifiedEvent, ObjectModifiedEvent,
    IObjectCopiedEvent, ObjectCopiedEvent)

from zope.app.container.contained import (
    IObjectAddedEvent, ObjectAddedEvent,
    IObjectMovedEvent, ObjectMovedEvent,
    IObjectRemovedEvent, ObjectRemovedEvent,
    IContainerModifiedEvent, ContainerModifiedEvent)

from martian import ClassGrokker, InstanceGrokker, GlobalGrokker
from grokcore.component import Adapter, MultiAdapter, GlobalUtility
from grok.components import Model, View
from grok.components import XMLRPC, REST, JSON
from grok.components import PageTemplate, PageTemplateFile, Traverser
from grok.components import Container, OrderedContainer
from grok.components import Site, LocalUtility, Annotation
from grok.components import Application, Form, AddForm, EditForm, DisplayForm
from grok.components import Indexes
from grok.components import Permission, Role, Public
from grok.components import Skin, IGrokLayer
from grok.components import RESTProtocol, IRESTLayer
from grok.interfaces import IRESTSkinType
from grok.components import ViewletManager, Viewlet

from martian import baseclass
from grokcore.component.directive import (
    context, name, title, description, provides, global_utility, direct)
from grok.directive import (
    template, templatedir, local_utility, permissions, require, site,
    layer, viewletmanager, view, traversable, order)
from grokcore.component.decorators import subscribe, adapter, implementer
from martian.error import GrokError, GrokImportError

# BBB These two functions are meant for test fixtures and should be
# imported from grok.testing, not from grok.
from grok.testing import grok, grok_component

from grok.formlib import action, AutoFields, Fields
from grok.util import url

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grok.interfaces import IGrokAPI
from zope.interface import moduleProvides
moduleProvides(IGrokAPI)
__all__ = list(IGrokAPI)
