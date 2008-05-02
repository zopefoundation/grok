"""
Trying to register two utilities for the same interface (and
potentially under the same name) will generate a configuration
conflict:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  ConfigurationConflictError: Conflicting configuration actions
    For: ('utility', <InterfaceClass grok.tests.utility.conflict.IUtilityInterface>, 'class and module')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grok.tests.utility.conflict.IUtilityInterface>, 'direct class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grok.tests.utility.conflict.IUtilityInterface>, 'explicit class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grok.tests.utility.conflict.IUtilityInterface>, 'implicit class')
  <BLANKLINE>
  <BLANKLINE>
    For: ('utility', <InterfaceClass grok.tests.utility.conflict.IUtilityInterface>, 'mixed class')
  <BLANKLINE>
  <BLANKLINE>

"""
import grok
from zope.interface import Interface, classProvides

class IUtilityInterface(Interface):
    pass

class IAnotherInterface(Interface):
    pass


class Implicit1(grok.GlobalUtility):
    grok.implements(IUtilityInterface)
    grok.name('implicit class')

class Implicit2(grok.GlobalUtility):
    grok.implements(IUtilityInterface)
    grok.name('implicit class')


class Explicit1(grok.GlobalUtility):
    grok.implements(IUtilityInterface, IAnotherInterface)
    grok.provides(IUtilityInterface)
    grok.name('explicit class')

class Explicit2(grok.GlobalUtility):
    grok.implements(IUtilityInterface, IAnotherInterface)
    grok.provides(IUtilityInterface)
    grok.name('explicit class')


class Mixed1(grok.GlobalUtility):
    grok.implements(IUtilityInterface, IAnotherInterface)
    grok.provides(IUtilityInterface)
    grok.name('mixed class')

class Mixed2(grok.GlobalUtility):
    grok.implements(IUtilityInterface)
    grok.name('mixed class')


class Direct1(grok.GlobalUtility):
    classProvides(IUtilityInterface)
    grok.name('direct class')
    grok.direct()

class Direct2(grok.GlobalUtility):
    classProvides(IUtilityInterface)
    grok.name('direct class')
    grok.direct()


class ClassLevel(grok.GlobalUtility):
    """This utility inherits from Grok's base class and is registered
    this way."""
    grok.implements(IUtilityInterface)
    grok.name('class and module')

class ModuleLevel(object):
    """This utility doesn't inherit from Grok's base class and is
    registered explicitly using the module-level directive below."""
    grok.implements(IUtilityInterface)

grok.global_utility(ModuleLevel, name='class and module')
