##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
from zope.component import adapts

from martian import ClassGrokker, InstanceGrokker, GlobalGrokker
from martian import baseclass
from martian.error import GrokError, GrokImportError

from grokcore.component import Context
from grokcore.component import GlobalUtility
from grokcore.component import Adapter, MultiAdapter, GlobalUtility, Context
from grokcore.component import Subscription, MultiSubscription
from grokcore.component import querySubscriptions, queryMultiSubscriptions
from grokcore.component import queryOrderedSubscriptions
from grokcore.component import queryOrderedMultiSubscriptions

from grokcore.component.decorators import subscribe, adapter, implementer
from grokcore.component import implements

from grokcore.component.directive import context, name, title, description
from grokcore.component.directive import provides, direct
from grokcore.component.directive import global_utility, global_adapter

from grokcore.content import Model, Container, OrderedContainer

from grokcore.security import Permission, Role
from grokcore.security import Public
from grokcore.security import require
from grokcore.security import permissions

from grokcore.view import ContentProvider
from grokcore.view import PageTemplate
from grokcore.view import PageTemplateFile
from grokcore.view import DirectoryResource
from grokcore.view import layer
from grokcore.view import template
from grokcore.view import templatedir
from grokcore.view import skin
from grokcore.view import url
from grokcore.view import path

from grokcore.viewlet import Viewlet
from grokcore.viewlet import ViewletManager
from grokcore.viewlet import view
from grokcore.viewlet import viewletmanager
from grokcore.viewlet import order

from grokcore.formlib import action
from grokcore.formlib import AutoFields
from grokcore.formlib import Fields

from grokcore.layout.interfaces import ILayout
from grokcore.layout import UnauthorizedPage
from grokcore.layout import NotFoundPage
from grokcore.layout import ExceptionPage
from grokcore.layout import layout

from grokcore.annotation import Annotation
from grokcore.annotation import queryAnnotation
from grokcore.annotation import deleteAnnotation
from grokcore.annotation import LazyAnnotation
from grokcore.annotation import LazyAnnotationProperty

from grokcore.site import IApplication
from grokcore.site import IApplicationAddedEvent
from grokcore.site import Application
from grokcore.site import ApplicationAddedEvent
from grokcore.site import getApplication
from grokcore.site import getSite
from grokcore.site import local_utility
from grokcore.site import install_on
from grokcore.site import LocalUtility
from grokcore.site import site
from grokcore.site import Site
from grokcore.site.util import create_application

from zope.event import notify

from zope.lifecycleevent import IObjectCopiedEvent
from zope.lifecycleevent import IObjectCreatedEvent
from zope.lifecycleevent import ObjectCopiedEvent
from zope.lifecycleevent import ObjectCreatedEvent

from zope.app.publication.interfaces import IBeforeTraverseEvent

from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.container.interfaces import IObjectAddedEvent
from zope.container.interfaces import IObjectMovedEvent
from zope.container.interfaces import IObjectRemovedEvent
from zope.container.contained import ObjectAddedEvent
from zope.container.contained import ObjectMovedEvent
from zope.container.contained import ObjectRemovedEvent

from grokcore.content import IObjectModifiedEvent
from grokcore.content import IContainerModifiedEvent
from grokcore.content import IObjectEditedEvent
from grokcore.content import ObjectModifiedEvent
from grokcore.content import ContainerModifiedEvent
from grokcore.content import ObjectEditedEvent

from grok.components import AddForm
from grok.components import AddFormPage
from grok.components import DisplayForm
from grok.components import DisplayFormPage
from grok.components import EditForm
from grok.components import EditFormPage
from grok.components import ExceptionView
from grok.components import Form
from grok.components import FormPage
from grok.components import Layout
from grok.components import NotFoundView
from grok.components import Page
from grok.components import UnauthorizedView
from grok.components import View

from grok.interfaces import IDatabaseCreatedEvent
from grok.events import DatabaseCreatedEvent

from grokcore.json import JSON
from grokcore.xmlrpc import XMLRPC

from grokcore.catalog import Indexes
from grokcore.catalog import index

from grokcore.traverser import Traverser
from grokcore.traverser import traversable

from grokcore.rest import IRESTLayer
from grokcore.rest import IRESTSkinType
from grokcore.rest import REST
from grokcore.rest import restskin

# BBB These two functions are meant for test fixtures and should be
# imported from grok.testing, not from grok.
from grok.testing import grok, grok_component

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grok.interfaces import IGrokAPI
from zope.interface import moduleProvides
moduleProvides(IGrokAPI)
__all__ = list(IGrokAPI)
