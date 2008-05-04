##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
"""Views for the grok admin UI"""

import grok
import os
import inspect
from urllib import urlencode

from grok.admin import docgrok
from grok.admin.docgrok import DocGrok, DocGrokPackage, DocGrokModule
from grok.admin.docgrok import DocGrokTextFile, DocGrokGrokApplication
from grok.admin.docgrok import DocGrokClass, DocGrokInterface, getItemLink

from grok.admin.objectinfo import ZopeObjectInfo
from grok.admin.utilities import getPathLinksForObject, getPathLinksForClass
from grok.admin.utilities import getPathLinksForDottedName, getParentURL

from ZODB.broken import Broken
from BTrees.OOBTree import OOBTree

import zope.component
from zope.interface import Interface
from zope.interface.interface import InterfaceClass
from zope.app.applicationcontrol.interfaces import IServerControl
from zope.app.applicationcontrol.applicationcontrol import applicationController
from zope.app.applicationcontrol.runtimeinfo import RuntimeInfo
from zope.app.applicationcontrol.browser.runtimeinfo import RuntimeInfoView
from zope.app.apidoc import utilities, codemodule
from zope.app.apidoc.utilities import getPythonPath, renderText, columnize
from zope.app.apidoc.codemodule.module import Module
from zope.app.apidoc.codemodule.class_ import Class
from zope.app.apidoc.codemodule.function import Function
from zope.app.apidoc.codemodule.text import TextFile
from zope.app.apidoc.codemodule.zcml import ZCMLFile
from zope.app.folder.interfaces import IRootFolder
from zope.app.security.interfaces import ILogout, IAuthentication
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.exceptions import DuplicationError
from zope.proxy import removeAllProxies
from zope.tal.taldefs import attrEscape

import z3c.flashmessage.interfaces


grok.context(IRootFolder)

class ManageApplications(grok.Permission):
    grok.name('grok.ManageApplications')

class Add(grok.View):
    """Add an application.
    """

    grok.require('grok.ManageApplications')

    def update(self, inspectapp=None, application=None):
        if inspectapp is not None:
            self.redirect(self.url("docgrok") + "/%s/index"%(application.replace('.','/'),))
        return

    def render(self, application, name, inspectapp=None):
        if name is None or name == "":
            self.redirect(self.url(self.context))
            return
        if name is None or name == "":
            self.redirect(self.url(self.context))
            return
        app = zope.component.getUtility(grok.interfaces.IApplication,
                                        name=application)
        try:
            self.context[name] = app()
            self.flash(u'Added %s `%s`.' % (application, name))
        except DuplicationError:
            self.flash(
                u'Name `%s` already in use. Please choose another name.' % (
                name,))
        self.redirect(self.url(self.context))


class Delete(grok.View):
    """Delete an application.
    """

    grok.require('grok.ManageApplications')

    def render(self, items=None):
        if items is None:
            self.redirect(self.url(self.context))
            return
        msg = u''
        if not isinstance(items, list):
            items = [items]
        for name in items:
            try:
                del self.context[name]
                msg = (u'%sApplication `%s` was successfully '
                       u'deleted.\n' % (msg, name))
            except AttributeError:
                # Object is broken.. Try it the hard way...
                # TODO: Try to repair before deleting.
                obj = self.context[name]
                if not hasattr(self.context, 'data'):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` attribute found.\n' % (msg, name))
                    continue
                if not isinstance(self.context.data, OOBTree):
                    msg = (
                        u'%sCould not delete application `%s`: no '
                        u'`data` is not a BTree.\n' % (msg, name))
                    continue
                self.context.data.pop(name)
                self.context.data._p_changed = True
                msg = (u'%sBroken application `%s` was successfully '
                       u'deleted.\n' % (msg, name))

        self.flash(msg)
        self.redirect(self.url(self.context))


class GAIAView(grok.View):
    """A grok.View with a special application_url.

    We have to compute the application_url different from common
    grok.Views, because we have no root application object in the
    adminUI. To avoid mismatch, we also call it 'root_url'.

    """

    def root_url(self, name=None):
        obj = self.context
        result = ""
        while obj is not None:
            if IRootFolder.providedBy(obj):
                return self.url(obj, name)
            obj = obj.__parent__
        raise ValueError("No application nor root element found.")

    def in_docgrok(self):
        return '/docgrok/' in self.url() or 'inspect.html' in self.url()

    def is_authenticated(self):
        """Check, wether we are authenticated.
        """
        return not IUnauthenticatedPrincipal.providedBy(self.request.principal)


class GrokAdminMacros(GAIAView):
    """Provides the o-wrap layout."""

    grok.context(Interface)



class Inspect(GAIAView):
    """Basic object browser.
    """

    grok.context(Interface)
    grok.name(u'inspect.html')
    grok.require('grok.ManageApplications')

    _metadata = None

    def update(self, show_private=False, *args, **kw):
        obj = self.context
        if isinstance(self.context, ZopeObjectInfo):
            # When the docgrok-object traverser delivers content, then
            # we get a wrapped context: the meant object is wrapped
            # into a ZopeObjectInfo.
            obj = self.context.obj

        self.ob_info = ZopeObjectInfo(obj)
        ob_info = self.ob_info
        self.show_private = show_private
        root_url = self.root_url()
        parent = ob_info.getParent()
        parent = {'class_link':
                      parent and getPathLinksForObject(parent) or '',
                  'obj_link' : getItemLink('',getParentURL(self.url(''))),
                  'obj' : parent
                  }
        bases = [getPathLinksForClass(x) for x in ob_info.getBases()]
        bases.sort()

        ifaces = [getPathLinksForClass(x) for x in
                  ob_info.getProvidedInterfaces()]
        ifaces.sort()

        methods = [x for x in list(ob_info.getMethods())
                   if self.show_private or not x['name'].startswith('_')]
        for method in methods:
            if method['interface']:
                method['interface'] = getPathLinksForDottedName(
                    method['interface'], root_url)
            if method['doc']:
                method['doc'] = renderText(method['doc'], getattr(obj,'__module__', None))

        attrs = [x for x in list(ob_info.getAttributes())
                 if self.show_private or not x['name'].startswith('_')
                 ]
        for attr in attrs:
            if '.' in str(attr['type']):
                attr['type'] = getPathLinksForClass(attr['type'], root_url)
            else:
                attr['type'] = attrEscape(str(attr['type']))
            if attr['interface']:
                attr['interface'] = getPathLinksForDottedName(
                    attr['interface'], root_url)
            attr['obj'] = getattr(obj, attr['name'], None)
            attr['docgrok_link'] = getItemLink(attr['name'], self.url(''))
        attrs.sort(lambda x,y: x['name']>y['name'])

        seqitems = ob_info.getSequenceItems() or []
        for item in seqitems:
            if '.' in str(item['value_type']):
                item['value_type'] = getPathLinksForClass(item['value_type'],
                                                          root_url)
            else:
                item['value_type'] = attrEscape(str(item['value_type']))
            item['obj'] = obj[item['index']]
            item['docgrok_link'] = getItemLink(item['index'], self.url(''))
        seqitems.sort()

        mapitems = [x for x in ob_info.getMappingItems()
                    if self.show_private or not x['key'].startswith('_')]
        for item in mapitems:
            if '.' in str(item['value_type']):
                item['value_type'] = getPathLinksForClass(item['value_type'],
                                                          root_url)
            else:
                item['value_type'] = attrEscape(str(item['value_type']))
            item['obj'] = obj[item['key']]
            item['docgrok_link'] = getItemLink(item['key'], self.url(''))
        mapitems.sort(lambda x,y: x['key']>y['key'])

        annotations = [x for x in ob_info.getAnnotationsInfo()
                    if self.show_private or not x['key'].startswith('_')]
        for item in annotations:
            if '.' in str(item['value_type']):
                item['value_type'] = getPathLinksForClass(item['value_type'],
                                                          root_url)
            else:
                item['value_type'] = attrEscape(str(item['value_type']))
            item['docgrok_link'] = getItemLink(item['key'], self.url(''))
        annotations.sort(lambda x,y: x['key']>y['key'])


        self.info = {
            'name' : ob_info.getId() or u'<unnamed object>',
            'type' : getPathLinksForClass((getattr(obj,
                                                   '__class__',
                                                   None)
                                           or type(obj)), root_url),
            'obj_link' : getPathLinksForObject(obj, root_url),
            'moduleinfo' : ob_info.getmoduleinfo(),
            'modulename' : ob_info.getmodulename(),
            'ismodule' : ob_info.ismodule(),
            'isclass' : ob_info.isclass(),
            'ismethod' : ob_info.ismethod(),
            'isfunction' : ob_info.isfunction(),
            'iscode' : ob_info.iscode(),
            'isbuiltin' : ob_info.isbuiltin(),
            'isroutine' : ob_info.isroutine(),
            'issequence' : ob_info.isSequence(),
            'ismapping' : ob_info.isMapping(),
            'isannotatable' : ob_info.isAnnotatable(),
            'doc' : renderText(ob_info.getdoc(),None),
            'comments' : ob_info.getcomments(),
            'module' : ob_info.getmodule(),
            'sourcefile' : ob_info.getsourcefile(),
            'source' : ob_info.getsource(),
            'parent' : parent,
            'dotted_path' : ob_info.getPythonPath(),
            'provided_interfaces' : ob_info.getDirectlyProvidedInterfaces(),
            'interfaces' : ifaces,
            'bases' : bases,
            'attributes' : attrs,
            'methods' : methods,
            'sequenceitems' : seqitems,
            'mappingitems' : mapitems,
            'annotations' : annotations
            }


class Index(GAIAView):
    """A redirector to the real frontpage."""

    grok.name('index.html') # The root folder is not a grok.Model
    grok.require('grok.ManageApplications')

    def update(self):
        apps = zope.component.getAllUtilitiesRegisteredFor(
            grok.interfaces.IApplication)
        self.applications = ("%s.%s" % (x.__module__, x.__name__)
                             for x in apps)
        # Go to the first page immediately.
        self.redirect(self.url('applications'))


class Applications(GAIAView):
    """View for application management.

    """

    grok.name('applications')
    grok.require('grok.ManageApplications')

    def getDocOfApp(self, apppath, headonly = True):
        doctor = docgrok.docgrok_handle(apppath)
        result = doctor.getDoc(headonly)
        if result is None:
            result = ""
        return result

    def update(self):
        from ZODB import broken

        from zope.app.broken.broken import IBroken

        # Available apps...
        apps = zope.component.getAllUtilitiesRegisteredFor(
            grok.interfaces.IApplication)
        self.applications = (
            {'name': "%s.%s" % (x.__module__, x.__name__),
             'docurl':("%s.%s" % (x.__module__, x.__name__)).replace('.', '/')}
            for x in apps)

        # Installed apps...
        inst_apps = [x for x in self.context.values()
                     if hasattr(x, '__class__') and x.__class__ in apps
                     and not issubclass(x.__class__, Broken)]
        inst_apps.sort(lambda x, y: cmp(x.__name__, y.__name__))
        self.installed_applications = inst_apps

        # Broken apps...
        broken_apps = [{'obj':y, 'name':x} for x,y in self.context.items()
                       if isinstance(y, Broken)]
        broken_apps.sort(lambda x, y: cmp(x['name'], y['name']))
        self.broken_applications = broken_apps


class AdminMessageSource(grok.GlobalUtility):

    grok.name('admin')
    zope.interface.implements(z3c.flashmessage.interfaces.IMessageSource)

    message = None

    def send(self, message, type='admin'):
        self.message = z3c.flashmessage.message.PersistentMessage(message,
                                                                  type)

    def list(self, type=None):
        if self.message is None:
            return
        if type is None or self.message.type == type:
            yield self.message

    def delete(self, message):
        if message is self.message:
            self.message = None
        else:
            raise KeyError(message)


class Server(GAIAView):
    """Zope3 management screen."""

    grok.require('grok.ManageApplications')

    @property
    def server_control(self):
        return zope.component.getUtility(IServerControl)

    @property
    def runtime_info(self):
        riv = RuntimeInfoView()
        riv.context = applicationController
        return riv.runtimeInfo()

    @property
    def current_message(self):
        source = zope.component.getUtility(
          z3c.flashmessage.interfaces.IMessageSource, name='admin')
        messages = list(source.list())
        if messages:
            return messages[0]

    def update(self, time=None, restart=None, shutdown=None,
              admin_message=None, submitted=False):
        if not submitted:
            return
        # Admin message control
        source = zope.component.getUtility(
          z3c.flashmessage.interfaces.IMessageSource, name='admin')
        if admin_message is not None:
            source.send(admin_message)
        elif getattr(source, 'current_message', False):
            source.delete(source.current_message)

        # Restart control
        if time is not None:
            try:
                time = int(time)
            except:
                time = 0
        else:
            time = 0

        if restart is not None:
            self.server_control.restart(time)
        elif shutdown is not None:
            self.server_control.shutdown(time)

        self.redirect(self.url())


class Users(GAIAView):
    """Users management screen."""

    grok.name('users')
    grok.require('grok.ManageApplications')

    def getPrincipals(self):
        from grok.admin import AUTH_FOLDERNAME, USERFOLDER_NAME

        sm = self.context.getSiteManager()
        if AUTH_FOLDERNAME not in list(sm.keys()):
            return []
        pau = sm[AUTH_FOLDERNAME]
        if USERFOLDER_NAME not in list(pau.keys()):
            return []
        userfolder = pau[USERFOLDER_NAME]
        users = list(userfolder.search({'search':''}))
        return [userfolder.principalInfo(x) for x in users]


    def update(self):
        self.principals = self.getPrincipals()
        pass



def getDottedPathDict(dotted_path):
    """Get a dict containing parts of a dotted path as links.
    """
    if dotted_path is None:
        return {}

    result = []
    part_path = ""
    for part in dotted_path.split('.'):
        name = part
        if part_path != "":
            name = "." + part
        part_path += part
        result.append({
            'name':name,
            'url':"/docgrok/%s" % (part_path,)
            })
        part_path += "/"
    return result


class DocGrokView(GAIAView):
    """A base DocGrok view.

    This view is used for all things not covered by other, more
    specialized views.
    """

    grok.context(DocGrok)
    grok.name('index')
    grok.require('grok.ManageApplications')

    def getDoc(self, text=None, heading_only=False):
        """Get the doc string of the module STX formatted."""
        if text is None:
            return None
            if (hasattr(self.context, "apidoc") and
                hasattr(self.context.apidoc, "getDocString")):
                text = self.context.apidoc.getDocString()
            else:
                return None
        lines = text.strip().split('\n')
        if len(lines) and heading_only:
            # Find first empty line to separate heading from trailing text.
            headlines = []
            for line in lines:
                if line.strip() == "":
                    break
                headlines.append(line)
            lines = headlines
        # Get rid of possible CVS id.
        lines = [line for line in lines if not line.startswith('$Id')]
        return renderText('\n'.join(lines), self.context.getPath())

    def getDocHeading(self, text=None):
        return self.getDoc(text, True)

    def getPathParts(self, path=None):
        """Get parts of a dotted name as url and name parts.
        """
        if path is None:
            path = self.context.path
        if path is None:
            return None
        return getDottedPathDict(path)
        result = []
        part_path = ""
        for part in path.split('.'):
            name = part
            if part_path != "":
                name = "." + part
            part_path += part
            result.append({
                'name':name,
                'url':"/docgrok/%s" % (part_path,)
                })
            part_path += "/"
        return result

    def getEntries(self, columns=True):
        """Return info objects for all modules and classes in the
        associated apidoc container.

        """
        if (not hasattr(self.context, "apidoc") or
            not hasattr(self.context.apidoc, "items")):
            return None
        entries = []
        for name, obj in self.context.apidoc.items():
            entry = {
                'name': name,
                'obj' : obj,
                'path': getPythonPath(removeAllProxies(obj)),
                'url' : u'',
                'doc' : None,
                'ispackage' : False,
                'ismodule' : False,
                'isinterface' : False,
                'isclass' : False,
                'isfunction' : False,
                'istextfile' : False,
                'iszcmlfile' : False,
                'signature' : None
                }
            entry['url'] = "%s/%s" % (self.context.path.replace('.','/'), name)
            if hasattr(obj,"getDocString"):
                entry['doc'] = self.getDocHeading(obj.getDocString())
            elif hasattr(obj, "getDoc") and isinstance(
                removeAllProxies(obj), InterfaceClass):
                entry['doc'] = self.getDocHeading(obj.getDoc())
            if isinstance(obj, Class):
                entry['isclass'] = True
            elif isinstance(obj, TextFile):
                entry['istextfile'] = True
            elif isinstance(obj, ZCMLFile):
                entry['iszcmlfile'] = True
            elif isinstance(obj,Function):
                entry['isfunction'] = True
                if hasattr(obj, 'getSignature'):
                    entry['signature'] = obj.getSignature()
            elif (isinstance(obj, Module) and
                  os.path.basename(obj.getFileName()) in
                    ['__init.py__', '__init__.pyc', '__init__.pyo']):
                entry['ispackage'] = True
            elif isinstance(obj, Module):
                entry['ismodule'] = True
            elif isinstance(obj, InterfaceClass):
                entry['isinterface'] = True
            entries.append(entry)

        entries.sort(lambda x, y: cmp(x['name'], y['name']))
        return entries

    def update(self):
        self.docgrok_root = self.context._traversal_root
        self.app_root = self.docgrok_root.__parent__
        pass


class DocGrokPackageView(DocGrokView):
    """A view for packages handled by DocGrok."""

    grok.context(DocGrokPackage)
    grok.name('index')


class DocGrokModuleView(DocGrokView):
    """A view for modules handled by DocGrok."""

    grok.context(DocGrokModule)
    grok.name('index')


class DocGrokClassView(DocGrokView):
    """A view for classes handled by DocGrok."""

    grok.context(DocGrokClass)
    grok.name('index')

    def getBases(self):
        return self._listClasses(self.context.apidoc.getBases())

    def getInterfaces(self):
        return self._listClasses(
          [iface for iface in self.context.apidoc.getInterfaces()])

    def getAttributes(self):
        attrs = self.context.getAttributes()
        for a in attrs:
            a['interface'] = self._listClasses([a['interface']])
        return attrs

    def getMethods(self):
        methods = self.context.getMethods()
        for m in methods:
            m['doc'] = renderText(m['attr'].__doc__ or '',
                                  inspect.getmodule(m['attr']))
            m['interface'] = self._listClasses([m['interface']])
        return methods

    def _listClasses(self, classes):
        info = []
        for cls in classes:
            unwrapped_cls = removeAllProxies(cls)
            fullpath = getPythonPath(unwrapped_cls)
            if not fullpath:
                continue
            path, name = fullpath.rsplit('.', 1)
            info.append({
                'path': path or None,
                'path_parts' : self.getPathParts(path) or None,
                'name': name,
                'url': fullpath and fullpath.replace('.','/') or None,
                'doc': self.getDocHeading(cls.__doc__) or None
                })
        return info


class DocGrokInterfaceView(DocGrokClassView):

    grok.context(DocGrokInterface)
    grok.name('index')


class DocGrokGrokApplicationView(DocGrokClassView):

    grok.context(DocGrokGrokApplication)
    grok.name('index')


class DocGrokTextFileView(DocGrokView):

    grok.context(DocGrokTextFile)
    grok.name('index')

    def getContent(self):
        lines = self.context.getContent()
        if self.context.path.endswith('.stx'):
            format = 'zope.source.stx'
        else:
            format = 'zope.source.rest'
        return renderText(lines, format=format)

    def getPackagePathParts(self):
        return self.getPathParts(
            self.context.getPackagePath())
