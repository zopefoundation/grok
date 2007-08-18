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
"""Information about objects.

This module provides wrappers/proies to give information about
objects at runtime. See inspect.txt to learn more about retrieving
object information using ObjectInfos.
"""
import inspect
import re
import types
from types import MethodType

import grok
from grok.admin.utilities import isContainingEvilRegExpChars

import zope
from zope.interface import Interface, implementedBy
from zope.interface.common.sequence import IExtendedReadSequence
from zope.interface.common.mapping import IEnumerableMapping
from zope.annotation.interfaces import IAnnotatable, IAnnotations
from zope.app.apidoc import utilities
from zope.location import location
from zope.schema import getFields
from zope.security.checker import getCheckerForInstancesOf
from zope.security.proxy import removeSecurityProxy
from zope.traversing.api import getParent, getRoot
from zope.traversing.interfaces import IPhysicallyLocatable
from zope.dublincore.interfaces import IZopeDublinCore
from zope.app.folder import rootFolder



class ObjectInfo(grok.Model):
    """An inspect proxy to provide object specific data.

    This is a base proxy, which can handle all (and only)
    Python-related data. See objectinfo.txt to learn more about
    ObjectInfos.
    """
    obj = None

    def __init__(self, obj):
        self.obj = obj

    def getmembers(self, predicate=None):
        """Return all the members of an object in a list of (name,
        value) pairs sorted by name.

        If the optional predicate argument is supplied, only members
        for which the predicate returns a true value are included.
        """
        return inspect.getmembers(self.obj, predicate)

    def getmoduleinfo(self):
        """Get information about modules.

        Return a tuple of values that describe how Python will
        interpret the file identified by path if it is a module, or
        None if it would not be identified as a module. The return
        tuple is (name, suffix, mode, mtype), where name is the name
        of the module without the name of any enclosing package,
        suffix is the trailing part of the file name (which may not be
        a dot-delimited extension), mode is the open() mode that would
        be used ('r' or 'rb'), and mtype is an integer giving the type
        of the module. mtype will have a value which can be compared
        to the constants defined in the imp module; see the
        documentation for that module for more information on module
        types.
        """
        path = getattr(self.obj, '__file__', None)
        if path is None:
            return None
        return inspect.getmoduleinfo(path)

    def getmodulename(self):
        """Return the name of the module named by the file path,
        without including the names of enclosing packages. This uses
        the same algorithm as the interpreter uses when searching for
        modules. If the name cannot be matched according to the
        interpreter's rules, None is returned.
        """
        path = getattr(self.obj, '__file__', None)
        if path is None:
            return None
        return inspect.getmodulename(path)

    def ismodule(self):
        """Return true if the object is a module.
        """
        return inspect.ismodule(self.obj)

    def isclass(self):
        """Return true if the object is a class.
        """
        return inspect.isclass(self.obj)

    def ismethod(self):
        """Return true if the object is a method.
        """
        return inspect.ismethod(self.obj)

    def isfunction(self):
        """Return true if the object is a Python function or unnamed
        (lambda) function.
        """
        return inspect.isfunction(self.obj)

    def istraceback(self):
        """Return true if the object is a traceback.
        """
        return inspect.istraceback(self.obj)

    def isframe(self):
        """Return true if the object is a frame.
        """
        return inspect.isframe(self.obj)

    def iscode(self):
        """Return true if the object is a code.
        """
        return inspect.iscode(self.obj)

    def isbuiltin(self):
        """Return true if the object is a built-in function.
        """
        return inspect.isbuiltin(self.obj)

    def isroutine(self):
        """Return true if the object is a user-defined or built-in
        function or method.
        """
        return inspect.isroutine(self.obj)

    def ismethoddescriptor(self):
        """Return true if the object is a method descriptor, but not
        if ismethod() or isclass() or isfunction() are true.

        This is new as of Python 2.2, and, for example, is true of
        int.__add__. An object passing this test has a __get__
        attribute but not a __set__ attribute, but beyond that the set
        of attributes varies. __name__ is usually sensible, and
        __doc__ often is.

        Methods implemented via descriptors that also pass one of the
        other tests return false from the ismethoddescriptor() test,
        simply because the other tests promise more - you can, e.g.,
        count on having the im_func attribute (etc) when an object
        passes ismethod().
        """
        return inspect.ismethoddescriptor(self.obj)

    def isdatadescriptor(self):
        """Return true if the object is a data descriptor.

        Data descriptors have both a __get__ and a __set__
        attribute. Examples are properties (defined in Python),
        getsets, and members. The latter two are defined in C and
        there are more specific tests available for those types, which
        is robust across Python implementations. Typically, data
        descriptors will also have __name__ and __doc__ attributes
        (properties, getsets, and members have both of these
        attributes), but this is not guaranteed. New in version 2.3.
        """
        return inspect.isdatadescriptor(self.obj)

    def isgetsetdescriptor(self):
        """Return true if the object is a getset descriptor.

        getsets are attributes defined in extension modules via
        PyGetSetDef structures. For Python implementations without
        such types, this method will always return False.

        New in version 2.5.
        """
        return inspect.isgetsetdescriptor(self.obj)

    def ismemberdescriptor(self):
        """Return true if the object is a member descriptor.

        Member descriptors are attributes defined in extension modules
        via PyMemberDef structures. For Python implementations without
        such types, this method will always return False.

        New in version 2.5.
        """
        return inspect.ismemberdescriptor(self.obj)

    #
    # Source code related...
    #
    def getdoc(self):
        """Get the documentation string for an object.

        All tabs are expanded to spaces. To clean up docstrings that
        are indented to line up with blocks of code, any whitespace
        than can be uniformly removed from the second line onwards is
        removed.
        """
        return inspect.getdoc(self.obj)

    def getcomments(self):
        """Get comments for an object.

        Return in a single string any lines of comments immediately
        preceding the object's source code (for a class, function, or
        method), or at the top of the Python source file (if the
        object is a module).

        Due to a bug in ``inspect.getsource()`` no objects can be
        handled, which contain a regular expression specific char in
        their string representation.

        """
        if isContainingEvilRegExpChars(str(self.obj)):
            return None
        return inspect.getcomments(self.obj)

    def getfile(self):
        """Return the name of the (text or binary) file in which an
        object was defined.

        If the object is a built-in module, class or function,
        ``None`` will be returned.
        """
        try:
            return inspect.getfile(self.obj)
        except TypeError:
            return

    def getmodule(self):
        """Try to guess which module an object was defined in.
        """
        return inspect.getmodule(self.obj)

    def getsourcefile(self):
        """Return the name of the Python source file in which an
        object was defined.

        If the object is a built-in module, class or function,
        ``None`` will be returned.
        """
        try:
            return inspect.getsourcefile(self.obj)
        except TypeError:
            return

    def getsourcelines(self):
        """Return a list of source lines and starting line number for
        an object.

        The argument may be a module, class, method, function,
        traceback, frame, or code object. The source code is returned
        as a list of the lines corresponding to the object and the
        line number indicates where in the original source file the
        first line of code was found. An IOError is raised if the
        source code cannot be retrieved.
        """
        try:
            return inspect.getsourcelines(self.obj)
        except TypeError:
            return
        return 

    def getsource(self):
        """Return the text of the source code for an object.

        The argument may be a module, class, method, function,
        traceback, frame, or code object. The source code is returned
        as a single string. An IOError is raised if the source code
        cannot be retrieved.

        Due to a bug in ``inspect.getsource()`` no objects can be
        handled, which contain a regular expression specific char in
        their string representation.
        """
        if isContainingEvilRegExpChars(str(self.obj)):
            return None

        try:
            return inspect.getsource(self.obj)
        except TypeError:
            return
        return

    def traverse(self, name):
        new_obj = None

        # Try to get name as dict entry...
        keygetter = getattr(self.obj, 'keys', None)
        if inspect.ismethod(keygetter):
            if name in keygetter():
                new_obj = self.obj[name]

        # Try to get name as sequence entry...
        if not new_obj:
            # This is not the appropriate way to handle iterators. We
            # must find somehing to handle them too.
            try:
                name_int = int(name)
                if name_int in range(0, len(self.obj)):
                    new_obj = self.obj[name_int]
            except ValueError:
                pass

        # Get name as obj attribute...
        if not new_obj and hasattr(self.obj, name):
            new_obj = getattr(self.obj, name, None)

        # Get name as annotation...
        if not new_obj:
            naked = zope.security.proxy.removeSecurityProxy(self.obj)
            try:
                annotations = IAnnotations(naked)
                new_obj = name and name in annotations and annotations[name]
                if not new_obj:
                    new_obj = annotations
            except TypeError:
                pass

        # Give obj a location...
        if new_obj:
            if not IPhysicallyLocatable(new_obj, False):
                new_obj = location.LocationProxy(
                    new_obj, self.obj, name)

            new_info = ZopeObjectInfo(new_obj)
            new_info.__parent__ = self
            new_info.__name__ = name
            return new_info

        # name not found...
        return





class ZopeObjectInfo(ObjectInfo):
    """Zope specific data.
    """

    def __init__(self, obj):
        self.obj = obj
        self.__klass = getattr(obj, '__class__', None) or type(obj)
        self.__interfaces = tuple(implementedBy(self.__klass))

    def getTypeLink(self, obj_type):
        if obj_type is types.NoneType:
            return None
        path = utilities.getPythonPath(obj_type)
        return path.replace('.', '/')

    def isLinkable(self, obj):
        """We consider all but some basic types to be linkable for docgrok.

        Although even simple strings can be displayed by a docgrok, it
        does not make much sense. We therefore simply forbid such
        links, filtering objects of basic types out.
        """
        for typespec in [types.NoneType, types.TypeType, types.BooleanType,
                         types.IntType, types.LongType, types.FloatType,
                         types.ComplexType, types.StringTypes,
                         types.MethodType, types.BuiltinFunctionType,
                         types.LambdaType, types.GeneratorType, types.CodeType,
                         types.FileType, types.TracebackType, types.FrameType,
                         types.BufferType, types.NotImplementedType]:
            if isinstance(obj, typespec):
                return False
        return True

    def getParent(self):
        return getParent(self.obj)

    def getPythonPath(self):
        return utilities.getPythonPath(self.obj)

    def getDirectlyProvidedInterfaces(self):
        # This comes from apidoc...
        # Getting the directly provided interfaces works only on naked objects
        naked = removeSecurityProxy(self.obj)
        return [utilities.getPythonPath(iface)
                for iface in zope.interface.directlyProvidedBy(naked)]

    def getProvidedInterfaces(self):
        return self.__interfaces

    def getBases(self):
        """Get base classes.
        """
        klass = getattr(self.obj, '__class__', None)
        return getattr(klass, '__bases__', None)

    def getAttributes(self):
        """Get all attributes of an object.

        See objectinfo.txt to learn more.
        """
        klass = removeSecurityProxy(self.__klass)
        obj = removeSecurityProxy(self.obj)
        for name in dir(obj):
            value = getattr(obj, name, None)
            if value is None:
                continue
            if inspect.ismethod(value) or inspect.ismethoddescriptor(value):
                continue
            entry = {
                'name': name,
                'value': `value`,
                'value_linkable': self.isLinkable(value),
                'type' : type(value),
                # type_link is a very browser oriented data
                # element. Move it to a view?
                'type_link': self.getTypeLink(type(value)),
                'interface': utilities.getInterfaceForAttribute(
                                 name, klass=klass)
                }
            entry.update(utilities.getPermissionIds(
                name, getCheckerForInstancesOf(klass)))
            yield entry

    def getMethods(self):
        """Get all methods of an object.

        Get a list of dicts, describing the methods of an object. The
        dicts support keys ``name`` (name of method), ``signature``,
        ``doc`` (method's docstring or ``None``) and ``interface``
        (the interface, where the method was defined or ``None``).
        """
        klass = removeSecurityProxy(self.__klass)
        obj = removeSecurityProxy(self.obj)
        for name in dir(obj):
            value = getattr(obj, name, None)
            if value is None:
                continue
            if not (inspect.ismethod(value)
                    and not inspect.ismethoddescriptor(value)):
                continue
            if inspect.ismethod(value):
                signature = utilities.getFunctionSignature(value)
            else:
                signature = '(...)'

            entry = {
                'name': name,
                'signature' : signature,
                'doc' : getattr(value, '__doc__', None),
                'interface': utilities.getInterfaceForAttribute(
                                 name, klass=klass),
                'value_linkable': self.isLinkable(value),
                }                
            entry.update(utilities.getPermissionIds(
                name, getCheckerForInstancesOf(klass)))
            yield entry
        
    def isSequence(self):
        """Is the object observed a sequence?
        """
        if isinstance(self.obj, types.ListType):
            return True
        if isinstance(self.obj, types.TupleType):
            return True
        return IExtendedReadSequence.providedBy(self.obj)

    def getSequenceItems(self):
        """Get the items of a sequence.

        Returns a list of dicts, each representing one element of the
        sequence.
        """
        if not self.isSequence():
            return
        
        elems = []
        naked = removeSecurityProxy(self.obj)
        for index in xrange(0, len(self.obj)):
            value = naked[index]
            elems.append({
                'index' : index,
                'value' : value,
                'value_type' : type(value),
                'value_type_link' : self.getTypeLink(type(value)),
                'value_linkable': self.isLinkable(value),
                })
        return elems

    def isMapping(self):
        """Is the object observed a mapping?

        Mappings are those objects, which are dicts or provide
        IEnumerableMapping.
        """
        if isinstance(self.obj, types.DictType):
            return True
        return IEnumerableMapping.providedBy(self.obj)

    def getMappingItems(self):
        """Get the elements of a mapping.

        The elements are delivered as a list of dicts, each dict
        containing the keys ``key``, ``key_string`` (the key as a
        string), ``value``, ``value_type`` and ``value_type_link``.
        """
        elems = []
        naked = removeSecurityProxy(self.obj)
        if not hasattr(naked, 'items'):
            return []
        for key, value in naked.items():
            elems.append({
                'key' : key,
                'key_string' : `key`,
                'value' : value,
                'value_type' : type(value),
                'value_type_link' : self.getTypeLink(type(value)),
                'value_linkable': self.isLinkable(value),
                })
        return elems

    def isAnnotatable(self):
        """Does the object observed expect to be annotated?
        """
        return IAnnotatable.providedBy(self.obj)


    def getAnnotationsInfo(self):
        """Get all annotations associated with an object.

        If no annotations are associated with the object, ``None`` is
        returned. Otherwise we get a list of dicts, each containing
        keys ``key``, ``key_string`` (textual representation of key),
        ``value``, ``value_type`` and ``value_type_link''.
        """
        if not self.isAnnotatable():
            return []
        naked = removeSecurityProxy(self.obj)
        annotations = IAnnotations(naked)
        if not hasattr(annotations, 'items'):
            return []
        elems = []
        for key, value in annotations.items():
            elems.append({
                'key' : key,
                'key_string' : `key`,
                'value' : value,
                'value_type' : type(value),
                'value_type_link' : self.getTypeLink(type(value)),
                'value_linkable': self.isLinkable(value),
                'obj' : annotations[key]
                })
        return elems

    def getId(self):
        """Try to determine some kind of name.
        """
        return (getattr(self.obj, '__name__', None)
               or getattr(self.obj, 'id', None)
               or getattr(self.obj, '_o_id', None))


from zope.traversing.interfaces import ITraversable
from zope.app.folder.interfaces import IRootFolder
from zope.location import LocationProxy
class AnnotationsTraverser(grok.Traverser):
    """If first URL element is '++anno++', handle over to
    ObjectBrowser.

    This traverser binds to the RootFolder, which means, it is only
    asked, when the publisher looks for elements in the Zope root (or
    another IRootFolder). The further traversing is done by the Docs'
    own traverser in it's model. See method `traverse()` in DocGrok.
    """
    grok.context(Interface)
    #grok.name('anno')
    #grok.provides(ITraversable)

    def traverse(self,path):
        namespace = 'anno'
        print "TRAVERSE", path
        if path.startswith(namespace):
            name = path[len(namespace):]
            naked = removeSecurityProxy(self.context)
            annotations = IAnnotations(naked)
            print annotations.items()
            #obj = name and annotations[name] or annotations
            #obj = path and annotations[name] or annotations
            obj = ObjectInfo("Hello")
            if not IPhysicallyLocatable(obj, False):
                #obj = LocationProxy(
                #    obj, self.context, namespace + name)
                obj = LocationProxy(
                    obj, self.context, 'anno' + name)
            return obj
        return

    def render(self):
        pass

##
## This comes from Dieter Maurer:
##

def determineClass(o):
  return hasattr(o, '__class__') and o.__class__ or type(o)

class Recorder(object):
  def __init__(self): self._account = {}
  def __call__(self, o):
    a = self._account
    class_ = determineClass(o)
    if class_ in a: a[class_] += 1
    else: a[class_] = 1
  def account(self): return self._account

def sortRecords(recorder):
  return sorted(recorder.account().items(), key=lambda r: r[1], reverse=True)

def fix((ty, no)):
  '''some types apparently have a broken 'str'. Fix this.'''
  try: tyn = str(ty)
  except TypeError:
    try: tyn = 'BROKEN-STR: %r' % ty
    except TypeError: tyn = 'BROKEN-STR-AND-REPR'
  return tyn, no

def analyseObjects(limit=100):
  '''analyses live objects and garbage.

  The result is a pair with information for live and garbage objects, respectively.
  The information is a dict with keys 'count' and 'sorted'.
  'count' is the total number of objects, 'sorted' a list with pairs
  'type' and 'instanceCount', inverse sorted by 'instanceCount'.
  '''
  result = []
  import gc
  for objs in gc.get_objects(), gc.garbage:
    r = Recorder()
    for o in objs: r(o)
    result.append({
      'count':len(objs),
      'sorted':map(fix, sortRecords(r)[:limit]),
      })
  return result












class ObjectInfo_obsolete(object):
    """A wrapper to provide object specific information.

    This is the base wrapper.
    
    See inspect.txt to learn more about this kind of thing.
    """

    def __init__(self, obj):
        self.obj = obj

    def getName(self):
        """Try to determine the name of an object.
        """
        for key in ['__name__', 'id', 'title', '_o_id']:
            name = getattr(self.obj, key, None)
            if name is not None:
                break
        return name

    def getDoc(self):
        """Fetch any doc strings from the wrapped object.
        """
        if hasattr(self.obj, '__class__'):
            return getattr(self.obj.__class__, '__doc__', None)
        return

    def getType(self):
        """Get the wrapped objects' type as a string in dotted path
        notation.
        """
        return type(self.obj)

    def getParent(self):
        """Get the parent of the wrapped object.

        This might result in a `TypeError` if the wrapped object is
        not locatable in sense of ILocation, i.e. if it doesn't
        provide ``__parent__`` attribute.
        """
        return getParent(self.obj)

    def getChildren(self):
        """Returns a list of children objects.
        """
        return dir(self.obj)

    def getRoot(self):
        """Get the root obj of the wrapped object.
        """
        try:
            return getRoot(self.obj)
        except TypeError:
            tmp = self.obj
            while getattr(tmp, '__parent__', None):
                tmp = tmp.__parent__
            return tmp
        return

    def isRoot(self):
        """Check, whether the wrapped object is the root within its branch.

        This does of course not necessarily mean, it is also the root
        of the whole instance.
        """
        try:
            return self.getRoot() == self.obj
        except TypeError:
            if getattr(self.obj, '__parent__', True) is None:
                return True
        return False

    def is_broken(self):
        """Check, whether the wrapped object is broken.
        """
        # XXX to be implemented.
        return


class DCObjectInfo(ObjectInfo_obsolete):
    """An object wrapper, that provides DublinCore related information.

    If such information is not available (for instance, because the
    type of object can't be adapted), None is returned for every
    value. It is therefore safe to use this info type also for objects
    not supporting DC.
    """
    obj = None
    supports_dc = False
    _metadata = None
    _covered_keys = [ 'created', 'modified', 'effective', 'expires',
                      'publisher', 'creators', 'subjects', 'contributors',
                      'description', 'title']


    def __init__(self, obj):

        super(ObjectInfo, self).__init__(obj)
        self.obj = obj
        try:
            dc = IZopeDublinCore(self.obj)
            self._metadata = dict((field, getattr(dc, field))
                                  for field in getFields(IZopeDublinCore) if hasattr(dc, field))
            self.supports_dc = True
        except TypeError:
            # A type error occurs, when obj can't be adapted to
            # IZopeDublinCore.
            self._metadata = dict([(x,None) for x in self._covered_keys])
                

    def _getDCEntry(self, category):
        if category in self._metadata.keys() and self._metadata[category]:
            return self._metadata[category]
        return



    def getDCMisc(self):
        """Get dict of DC metadata not covered by other methods.
        """
        return dict([x for x in self._metadata.items()
                     if x[0] not in self.covered_keys])

    def getDCTitle(self):
        return self._getDCEntry('title') or u''

    def getDCDescription(self):
        return self._getDCEntry('description') or u''

    def getDCCreators(self):
        return self._getDCEntry('creators') or ()

    def getDCContributors(self):
        return self._getDCEntry('contributors') or ()

    def getDCSubjects(self):
        return self._getDCEntry('subjects') or ()

    def getDCPublisher(self):
        return self._getDCEntry('publisher') or u''

    def getDCCreationDate(self):
        return self._getDCEntry('created') or u''

    def getDCModificationDate(self):
        return self._getDCEntry('modified') or u''

    def getDCEffectiveDate(self):
        return self._getDCEntry('effective') or u''

    def getDCExpiringDate(self):
        return self._getDCEntry('expires') or u''

