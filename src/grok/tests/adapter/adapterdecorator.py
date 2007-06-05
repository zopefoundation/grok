"""
@grok.adapter can only be used on module level::

  >>> function_context()
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.adapter can only be used on module level.

  >>> class_context()
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.adapter can only be used on module level.

  >>> @grok.adapter(Cave)
  ... def func():
  ...     pass
  Traceback (most recent call last):
    ...
  GrokImportError: @grok.implementer should be used as inner decorator.

  >>> grok.grok(__name__)
  >>> cave = Cave()
  >>> home = IHome(cave)
  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True
  >>> anotherhome = IAnotherHome(cave)
  >>> IHome.providedBy(anotherhome)
  True
  >>> isinstance(anotherhome, Home)
  True
  >>> morehome = IMoreHome(cave)
  >>> IHome.providedBy(morehome)
  True
  >>> isinstance(morehome, Home)
  True
"""

import grok
from zope import interface

class IDummy(interface.Interface):
    pass

def function_context():
    @grok.adapter(IDummy)
    @grok.implementer(IDummy)
    def subscriber():
        pass

def class_context():
    class Wrapper:
        @grok.adapter(IDummy)
        @grok.implementer(IDummy)
        def subscriber(self):
            pass

class ICave(interface.Interface):
    pass

class IHome(interface.Interface):
    pass

class IAnotherHome(interface.Interface):
    pass

class IMoreHome(interface.Interface):
    pass

class Cave(grok.Model):
    grok.implements(ICave)
    pass

class Home(object):
    grok.implements(IHome)

@grok.adapter(Cave)
@grok.implementer(IHome)
def home_for_cave(cave):
    return Home()

@grok.adapter
@grok.implementer(IAnotherHome)
def another_home_for_cave(cave):
    return Home()

@grok.adapter(ICave)
@grok.implementer(IMoreHome)
def more_home_for_cave(cave):
    return Home()
