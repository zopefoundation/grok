"""
When refering to a class in the grok.require() directive, this class needs
to implement the zope.security.interfaces.IPermission interface::

  >>> from zope.interface import Interface
  >>> class NotAProperPermission(object):
  ...   pass
  >>>
  >>> class NoPermission(grok.View):
  ...     grok.context(zope.interface.Interface)
  ...     grok.require(NotAProperPermission)
  ...
  ...     def render(self):
  ...         pass
  Traceback (most recent call last):
  ...
  GrokImportError: You can only pass unicode, ASCII, or a subclass of
  grok.Permission to the 'require' directive.

"""

import grok
import zope.interface
