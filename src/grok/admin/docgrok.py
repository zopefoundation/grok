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
"""The Grok's Friendly Doctor.

Ask DocGrok and he will try his best, to keep you well informed about
everything hanging around in your Zope3 and your Grok Application.

See file `docgrok.txt` in this package to learn more about docgrok.

"""

import os
import sys # for sys.path
import types
import grok
import inspect
from urlparse import urlparse, urlunparse

import zope.component
from zope.app.folder.interfaces import IRootFolder
from zope.dottedname.resolve import resolve
from zope.interface.interface import InterfaceClass
from zope.security.proxy import isinstance
from zope.security.proxy import removeSecurityProxy
from zope.proxy import removeAllProxies

from zope.app.apidoc.codemodule.module import Module
from zope.app.apidoc.codemodule.class_ import Class
from zope.app.apidoc.codemodule.text import TextFile
from zope.app.apidoc.utilities import renderText
from zope.app.apidoc.utilities import getFunctionSignature
from zope.app.apidoc.utilities import getPythonPath, getPermissionIds
from zope.app.apidoc.utilities import isReferencable

import grok.interfaces
from grok.interfaces import IApplication
from martian.scan import is_package, ModuleInfo
from martian import ClassGrokker, ModuleGrokker
from grok.admin.objectinfo import ZopeObjectInfo

# This is the name under which the docgrok object-browser can be
# reached.
DOCGROK_ITEM_NAMESPACE = 'docgrok-obj'

grok.context(IRootFolder)

def find_filepath(dotted_path):
    """Find the filepath for a dotted name.

    If a dotted name denotes a filename we try to find its path
    by concatenating it with the system paths and looking for an
    existing file. Every dot in the filename thereby can be part
    of the filename or of its path. Therefore we check the
    several possible dirname/filename combinations possible.

    Returns None if no suitable filepath can be found.

    This functions does *not* look for Python elements like classes,
    interfaces and the files where they were defined. Use `resolve()`
    and the `__file__` attribute for examining this kind of stuff
    instead.

    This function finds the location of text files and the like, as
    far as they are placed inside some Python path.
    """
    currpath = dotted_path
    currname = ""
    while '.' in currpath:
        currpath, name = currpath.rsplit('.', 1)
        if currname != "":
            currname = "." + currname
        currname = name + currname
        tmp_path = ""
        for elem in currpath.split('.'):
            tmp_path = os.path.join(tmp_path, elem)
        for syspath in sys.path:
            filepath_to_check = os.path.join(syspath, tmp_path, currname)
            if os.path.isfile(filepath_to_check):
                return filepath_to_check
    return None

class DocGrokHandler(object):
    """A handler for DocGrok objects.

    The solely purpose of DocGrokHandlers is to determine, whether a
    given dotted path denotes a special type of object. If so, it
    should pass back an appropriate DocGrok object.

    In plain English: DocGrokHandlers find a doctor for any object.

    All we expect a DocGrokHandler to support, is a method
    ``getDoctor``, which takes a dotted path (and optional the object
    denoted by this path), to deliver an appropriate doctor or
    ``None``.
    """
    def getDoctor(self, dotted_path, obj=None):
        """The default docfinder cannot serve.
        """
        return


class DocGrokModuleHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Find a doctor for modules or None, if the dotted_path does
        not denote a module.
        """
        if obj is None:
            try:
                obj = resolve(dotted_path)
            except ImportError:
                return
        if not hasattr(obj, '__file__'):
            return
        if not is_package(os.path.dirname(obj.__file__)):
            return
        if os.path.basename(obj.__file__) in ['__init__.py',
                                             '__init__.pyc',
                                             '__init__.pyo']:
            return
        return DocGrokModule(dotted_path)


class DocGrokPackageHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Determine, whether the given path/obj references a Python
        package.
        """
        if obj is None:
            try:
                obj = resolve(dotted_path)
            except ImportError:
                return
        if not hasattr(obj, '__file__'):
            return
        if not is_package(os.path.dirname(obj.__file__)):
            return
        if os.path.basename(obj.__file__) not in ['__init__.py',
                                                 '__init__.pyc',
                                                 '__init__.pyo']:
            return
        return DocGrokPackage(dotted_path)


class DocGrokInterfaceHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Determine, whether the given path/obj references an interface.
        """
        if obj is None:
            try:
                obj = resolve(dotted_path)
            except ImportError:
                return
        if not isinstance(
            removeAllProxies(obj), InterfaceClass):
            return
        return DocGrokInterface(dotted_path)


class DocGrokClassHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Determine, whether the given path/obj references a Python class.
        """
        if obj is None:
            try:
                obj = resolve(dotted_path)
            except ImportError:
                return
        if not isinstance(obj, (types.ClassType, type)):
            return
        return DocGrokClass(dotted_path)


class DocGrokGrokApplicationHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Determine, whether the given path/obj references a Grok application.
        """
        if obj is None:
            try:
                obj = resolve(dotted_path)
            except ImportError:
                None
        try:
            if not IApplication.implementedBy(obj):
                return
        except TypeError:
            return
        return DocGrokGrokApplication(dotted_path)


class DocGrokTextFileHandler(DocGrokHandler):
    def getDoctor(self, dotted_path, obj=None):
        """Determine whether the dotted_path denotes a textfile.
        """
        if obj is not None:
            # Textfiles that are objects, are not text files.
            return
        if os.path.splitext(dotted_path)[1] != u'.txt':
            return
        return DocGrokTextFile(dotted_path)


def docgrok_handle(dotted_path):
    """Find a doctor specialized for certain things.
    """
    try:
        ob = resolve(dotted_path)
    except ImportError:
        # There is no object of that name. Give back 404.
        # TODO: Do something more intelligent, offer a search.
        if not find_filepath(dotted_path):
            return
        ob = None
    except:
        return

    for handler in docgrok_handlers:
        if type(handler) is not type({}):
            continue
        if 'docgrok_handler' not in handler.keys():
            continue
        spec_handler = handler['docgrok_handler']()
        if not isinstance(spec_handler, DocGrokHandler):
            continue
        doc_grok = spec_handler.getDoctor(dotted_path, ob)
        if doc_grok is None:
            continue
        return doc_grok
    # No special doctor could be found.
    return DocGrok(dotted_path)

def getInterfaceInfo(iface):
    if iface is None:
        return
    path = getPythonPath(iface)
    return {'path': path,
            'url': isReferencable(path) and path or None}


class DocGrokGrokker(ClassGrokker):
    """A grokker that groks DocGroks.

    This grokker can help to 'plugin' different docgroks in an easy
    way. You can register docgroks for your special classes, modules,
    things. All required, is a function, that determines the correct
    kind of thing, you like to offer a docgrok for and returns a
    specialized docgrok or None (in case the thing examined is not the
    kind of thing your docgrok is a specialist for).

    Unfortunately, order counts here. If one docgrok handler is able
    to deliver a specialized docgrok object, no further invesitgation
    will be done.

    In principle, the following should work. First we import the
    docgrok module, because it contains a more specific grokker: the
    InstanceGrokker 'docgrok_grokker' ::

      >>> from grok.admin import docgrok

    Then we create an (empty) 'ModuleGrokker'. 'ModuleGrokkers' can
    grok whole modules. ::

      >>> from martian import ModuleGrokker
      >>> module_grokker = ModuleGrokker()

    Then we register the 'docgrok_grokker', which should contain some
    base handlers for modules, classes, etc. by default::

      >>> module_grokker.register(docgrok.docgrok_handler_grokker)

    The 'docgrok_handler_grokker' is an instance of 'DocGrokGrokker'::

      >>> from grok.admin.docgrok import DocGrokGrokker
      >>> isinstance(docgrok.docgrok_handler_grokker, DocGrokGrokker)
      True

    That's it.

    """
    component_class = DocGrokHandler

    def grok(self, name, obj, **kw):
        if not issubclass(obj, DocGrokHandler):
            return
        if not hasattr(obj, 'getDoctor'):
            return
        docgrok_handlers.insert(0, {'name':name,
                                    'docgrok_handler':obj})
        return True


class DocGrok(grok.Model):
    """DocGrok helps us finding out things about ourselves.

    There are DocGroks for packages, modules, interfaces, etc., each
    one a specialist for a certain type of element. 'Pure' DocGroks
    build the root of this specialist hierarchy and care for objects,
    which can not be handled by other, more specialized DocGroks.

    DocGrok offers a minimum of information but can easily be extended in
    derived classes.
    """
    path = None
    _traversal_root = None

    def __init__(self, dotted_path):
        self.path = dotted_path

    def getPath(self):
        return self.path

    def getFilePath(self):
        try:
            ob = resolve(self.path)
            return hasattr(ob, __file__) and os.path.dirname(ob.__file__) or None
        except ImportError:
            pass
        return find_filepath(self.path)

    def getDoc(self, heading_only=False):
        """Get the doc string of the module STX formatted.
        """
        if hasattr(self, "apidoc") and hasattr(
            self.apidoc, "getDocString"):
            text = self.apidoc.getDocString()
        else:
            return
        if text is None:
            return
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
        return renderText('\n'.join(lines), self.path)


    def traverse(self,patient):
        """ Do special traversing inside the surgery.

        Inside the docgrok-'namespace' we only accept DocGroks and
        colleagues. Each DocGrok cares for a patient represented by a
        path. This path might denote an object in the ZODB or in the
        python path.

        """
        if patient == "index.html":
            return self
        if self.path is None:
            newpath = patient
        else:
            newpath = '.'.join([self.path, patient])

        doctor = docgrok_handle(newpath)

        if doctor is None:
            # There is nothing of that name. Give back 404.
            # XXX Do something more intelligent, offer a search.
            return
        doctor.__parent__ = self
        doctor.__name__ = patient
        doctor._traversal_root = self._traversal_root
        doctor.path = newpath
        return doctor
    pass

def getItemLink(name, baseurl):
    """Get a link to a docgrok item out of an item name and a base URL.

    A docgrok item is any object, which is a 'subobject' of another
    object, for example an attribute, a memberfunction, an annotation
    or a sequence item (if the parent object is a sequence). Those
    objects are not neccessarily directly accessible, but need to be
    denoted for the object browser. We put 'docgrok-item' as marker at
    the beginning of the URL to enable the docgrok traverser and to
    handle those URLs in a special way. Such the objectbrowser can
    handle those 'unaccessible' items.
    """
    url = list(urlparse(baseurl))
    path = url[2]
    if path.startswith('/' + DOCGROK_ITEM_NAMESPACE + '/'):
        path = path[len(DOCGROK_ITEM_NAMESPACE) + 2:]
    if path.endswith('/@@inspect.html') or path.endswith('/inspect.html'):
        path = path.rsplit('/', 1)
    path = "/%s/%s%s/@@inspect.html" % (DOCGROK_ITEM_NAMESPACE, path, name)
    path = path.replace('//', '/')
    url[2] = path
    return urlunparse(url)


class DocGrokTraverser(grok.Traverser):
    """If first URL element is 'docgrok', handle over to DocGrok.

    This traverser binds to the RootFolder, which means, it is only
    asked, when the publisher looks for elements in the Zope root (or
    another IRootFolder). The further traversing is done by the Docs'
    own traverser in it's model. See method `traverse()` in DocGrok.
    """
    grok.context(IRootFolder)

    def traverse(self,path):
        if path == DOCGROK_ITEM_NAMESPACE:
            # The objectbrowser is called...
            obj_info = ZopeObjectInfo(self.context)
            obj_info.__parent__ = self.context
            obj_info.__name__ = DOCGROK_ITEM_NAMESPACE
            return obj_info

        if path == "docgrok":
            doctor = DocGrok(None)
            # Giving a __parent__ and a __name__, we make things
            # locatable in sense of ILocatable.
            doctor.__parent__ = self.context
            doctor.__name__ = 'docgrok'
            doctor._traversal_root = doctor
            return doctor
        return


class DocGrokPackage(DocGrok):
    """This doctor cares for python packages.
    """
    path=None
    apidoc = None
    _traversal_root = None

    def __init__(self,dotted_path):
        self.path = dotted_path
        self._module = resolve(self.path)
        # In apidoc packages are handled like modules...
        self.apidoc = Module(None, None, self._module, True)

    def getDocString(self):
        return self.apidoc.getDocString()

    def getFilePath(self):
        ob = resolve(self.path)
        return os.path.dirname(ob.__file__) + '/'

    def _getModuleInfos(self, filter_func=lambda x:x):
        """Get modules and packages of a package.

        The filter function will be applied to a list of modules and
        packages of type grok.scan.ModuleInfo.
        """
        ob = resolve(self.path)
        filename = ob.__file__
        module_info = ModuleInfo(filename, self.path)
        try:
            infos = module_info.getSubModuleInfos(exclude_tests=False)
        except TypeError:
            # Another version of martian.scan is installed
            infos = module_info.getSubModuleInfos()
        if filter_func is not None:
            infos = filter(filter_func, infos)
        result = []
        for info in infos:
            subresult = {}
            # Build a url string from dotted path...
            mod_path = "docgrok"
            for path_part in info.dotted_name.split('.'):
                mod_path = os.path.join(mod_path, path_part)
            subresult = {
                'url' : mod_path,
                'name' : info.name,
                'dotted_name' : info.dotted_name
                }
            result.append(subresult)
        return result


    def getModuleInfos(self):
        """Get the modules inside a package.
        """
        filter_func = lambda x: not x.isPackage()
        return self._getModuleInfos(filter_func)

    def getSubPackageInfos(self):
        """Get the subpackages inside a package.
        """
        filter_func = lambda x: x.isPackage()
        return self._getModuleInfos(filter_func)

    def getTextFiles(self):
        """Get the text files inside a package.
        """
        filter_func = lambda x: x.isinstance(TextFile)
        return self._getModuleInfos(filter_func)

    def getChildren(self):
        result = self.apidoc.items()
        result.sort(lambda x,y:cmp(x[0], y[0]))
        return result



class DocGrokModule(DocGrokPackage):
    """This doctor cares for python modules.
    """

    def getFilePath(self):
        ob = resolve(self.path)
        filename = ob.__file__
        if filename.endswith('o') or filename.endswith('c'):
            filename = filename[:-1]
        return filename


class DocGrokClass(DocGrokPackage):
    """This doctor cares for classes.
    """
    def __init__(self,dotted_path):
        self.path = dotted_path
        self.klass = resolve(self.path)
        self.module_path, self.name = dotted_path.rsplit('.',1)
        self.module = resolve(self.module_path)
        mod_apidoc = Module(None, None, self.module, False)
        self.apidoc = Class(mod_apidoc, self.name, self.klass)

    def getFilePath(self):
        if not hasattr(self.module, "__file__"):
            return
        filename = self.module.__file__
        if filename.endswith('o') or filename.endswith('c'):
            filename = filename[:-1]
        return filename

    def getAttributes(self):
        """Get the attributes of this class."""
        attrs = []
        # See remark in getMethods()
        klass = removeSecurityProxy(self.apidoc)
        for name, attr, iface in klass.getAttributes():
            entry = {'name': name,
                     'value': `attr`,
                     'type': type(attr).__name__,
                     'interface': iface
                }
            entry.update(getPermissionIds(name,klass.getSecurityChecker()))
            attrs.append(entry)
        return attrs

    def getMethods(self):
        """Get all methods of this class."""
        methods = []
        # remove the security proxy, so that `attr` is not proxied. We could
        # unproxy `attr` for each turn, but that would be less efficient.
        #
        # `getPermissionIds()` also expects the class's security checker not
        # to be proxied.
        klass = removeSecurityProxy(self.apidoc)
        for name, attr, iface in klass.getMethodDescriptors():
            entry = {'name': name,
                     'signature': "(...)",
                     'doc':attr.__doc__ or '',
                     'attr' : attr,
                     'interface' : iface}
            entry.update(getPermissionIds(name, klass.getSecurityChecker()))
            methods.append(entry)

        for name, attr, iface in klass.getMethods():
            entry = {'name': name,
                     'signature': getFunctionSignature(attr),
                     'doc':attr.__doc__ or '',
                     'attr' : attr,
                     'interface' : iface}
            entry.update(getPermissionIds(name, klass.getSecurityChecker()))
            methods.append(entry)
        return methods


class DocGrokInterface(DocGrokClass):
    """This doctor cares for interfaces.
    """
    def __init__(self,dotted_path):
        self.path = dotted_path
        self.klass = resolve(self.path)
        self.module_path, self.name = dotted_path.rsplit('.',1)
        self.module = resolve(self.module_path)
        mod_apidoc = Module(None, None, self.module, False)
        self.apidoc = Class(mod_apidoc, self.name, self.klass)

    def getFilePath(self):
        if not hasattr(self.module, "__file__"):
            return
        filename = self.module.__file__
        if filename.endswith('o') or filename.endswith('c'):
            filename = filename[:-1]
        return filename

class DocGrokGrokApplication(DocGrokClass):
    """This doctor cares for Grok applications and components.
    """
    pass

class DocGrokTextFile(DocGrok):
    """This doctor cares for text files.
    """

    def __init__(self,dotted_path):
        self.path = dotted_path
        self.filepath = find_filepath(self.path)
        self.filename = os.path.basename(self.filepath)


    def getPackagePath(self):
        """Return package path as dotted name.
        """
        dot_num_in_filename = len([x for x in self.filename if x == '.'])
        parts = self.path.rsplit('.', dot_num_in_filename + 1)
        return parts[0]

    def getContent(self):
        """Get file content UTF-8 encoded.
        """
        file = open(self.filepath, 'rU')
        content = file.read()
        file.close()
        return content.decode('utf-8')

# The docgroks registry.
#
# We register 'manually', because the handlers
# are defined in the same module.
docgrok_handlers = []

docgrok_handler_grokker = DocGrokGrokker()
docgrok_handler_grokker.grok('module', DocGrokModuleHandler)
docgrok_handler_grokker.grok('package', DocGrokPackageHandler)
docgrok_handler_grokker.grok('interface', DocGrokInterfaceHandler)
docgrok_handler_grokker.grok('class', DocGrokClassHandler)
docgrok_handler_grokker.grok('grokapplication',
                             DocGrokGrokApplicationHandler)
docgrok_handler_grokker.grok('textfile', DocGrokTextFileHandler)
docgrok_handlers_grokker = ModuleGrokker()
docgrok_handlers_grokker.register(docgrok_handler_grokker)

