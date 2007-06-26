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

from zope.interface import Interface, Attribute

class IGrokker(Interface):
    priority = Attribute('Priority during module grokking.')

    def grok(name, obj, **kw):
        """Grok obj.

        name - name of object (in module)
        obj - object to grok
        **kw - optional parameters passed along the grokking process.

        May do extra filtering based on name or obj.

        Returns True if grok is attempted, False if object is filtered
        out by this grokker.
        """
    
class IComponentGrokker(IGrokker):
    """A grokker that groks components in a module.

    Components may be instances or classes indicated by component_class.
    """
    component_class = Attribute('Class of the component to match')
    
class IMultiGrokker(IComponentGrokker):
    """A grokker that is composed out of multiple grokkers.
    """
    def register(grokker):
        """Register a grokker.
        """

    def clear():
        """Clear all grokkers and go back to initial state.
        """

    def grokkers(name, obj):
        """Iterable of all grokkers that apply to obj.
        """

class IModuleInfo(Interface):
    def getModule():
        """Get the module object this module info is representing.

        In case of packages, gives back the module object for the package's
        __init__.py
        """

    def isPackage():
        """Returns True if this module is a package.
        """

    def getSubModuleInfos():
        """Get module infos for any sub modules.

        In a module, this will always return an empty list.
        """

    def getSubModuleInfo(name):
        """Get sub module info for <name>.

        In a package, give module info for sub-module.
        Returns None if no such sub module is found. In a module,
        always returns None.
        """

    def getResourcePath(name):
        """Get the absolute path of a resource directory.

        The resource directory will be 'relative' to this package or
        module.

        Case one: get the resource directory with name <name> from the same
        directory as this module

        Case two: get the resource directory with name <name> from the children
        of this package
        """

    def getAnnotation(key, default):
        """Given a key, get annotation object from module.

        The annotation key is a dotted name. All dots are replaced
        with underscores and the result is pre and post-fixed by
        double underscore. For instance 'grok.name' will be translated
        to '__grok_name__'.
        
        Uses default if no such annotation found.
        """

