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
from grok.components import Model, Adapter, MultiAdapter, View, XMLRPC, JSON
from grok.components import PageTemplate, PageTemplateFile, Container, Traverser
from grok.components import Site, GlobalUtility, LocalUtility, Annotation
from grok.components import Application, Form, AddForm, EditForm, DisplayForm
from grok.components import Indexes
from grok.components import Permission, Role
from grok.components import Skin, IGrokLayer
from grok.directive import (context, name, title, template, templatedir,
                            provides, baseclass, global_utility, local_utility,
                            permissions, require, site, layer, localesdir)
from grok._grok import do_grok as grok  # Avoid name clash within _grok
from grok._grok import grok_component
from grok._grok import SubscribeDecorator as subscribe
from grok._grok import adapter, implementer
from martian.error import GrokError, GrokImportError

from grok.formlib import action, AutoFields, Fields
from grok.util import url

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grok.interfaces import IGrokAPI
from zope.interface import moduleProvides
moduleProvides(IGrokAPI)
__all__ = list(IGrokAPI)
