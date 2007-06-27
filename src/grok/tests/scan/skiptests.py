"""
By default functional tests and unit tests are skipped from the grokking
procedure.

Packages called 'tests' (the "de facto" standard name for packages containing
unit tests) or 'ftests' (for functional tests) are skipped (and thus not
grokked)::

  >>> from grok.scan import ModuleInfo, module_info_from_dotted_name
  >>> module_info = module_info_from_dotted_name(
  ...     'grok.tests.scan.withtestspackages')
  >>> module_info
  <ModuleInfo object for 'grok.tests.scan.withtestspackages'>
  >>> # Will *not* contain the module info for the tests and ftests packages
  >>> print module_info.getSubModuleInfos()
  [<ModuleInfo object for 'grok.tests.scan.withtestspackages.subpackage'>]

Likewise modules called tests.py or ftests.py are skipped::

  >>> from grok.scan import ModuleInfo, module_info_from_dotted_name
  >>> module_info = module_info_from_dotted_name(
  ...     'grok.tests.scan.withtestsmodules')
  >>> module_info
  <ModuleInfo object for 'grok.tests.scan.withtestsmodules'>
  >>> # Will *not* contain the module info for the tests and ftests modules
  >>> print module_info.getSubModuleInfos()
  [<ModuleInfo object for 'grok.tests.scan.withtestsmodules.subpackage'>]

You can still get to the module info of tests and ftests if you need to::

  >>> module_info = module_info_from_dotted_name(
  ...     'grok.tests.scan.withtestspackages')
  >>> module_info
  <ModuleInfo object for 'grok.tests.scan.withtestspackages'>
  >>> print module_info.getSubModuleInfos(exclude_tests=False)
  [<ModuleInfo object for 'grok.tests.scan.withtestspackages.ftests'>,
  <ModuleInfo object for 'grok.tests.scan.withtestspackages.subpackage'>,
  <ModuleInfo object for 'grok.tests.scan.withtestspackages.tests'>]

Skipped tests and ftests pacakges are not grokked as part of the grokking
procedure of the "parent" packages. The registrations therein will not be made::

  >>> import grok
  >>> grok.grok('grok.tests.scan.withtestspackages')
  >>> from zope import component
  >>> from grok.tests.scan.withtestspackages.tests import IMammoth
  >>> # Test by trying to retrieve a global utility, which is not there
  >>> component.getUtility(IMammoth)
  Traceback (most recent call last):
  ...
  ComponentLookupError:
  (<InterfaceClass grok.tests.scan.withtestspackages.tests.IMammoth>, '')

However, tests and ftests can still be grokked when explicitely called for
(e.g. *inside* tests and ftests - the very fact the other test cases work is
already proof of this, but still)::

  >>> grok.grok('grok.tests.scan.withtestspackages.tests')
  >>> from zope import component
  >>> from grok.tests.scan.withtestspackages.tests import IMammoth
  >>> # Test by trying to retrieve a global utility
  >>> component.getUtility(IMammoth)
  <grok.tests.scan.withtestspackages.tests.Mammoth object at ...>

Likewise tests and ftests modules are not grokked as part of the grokking
procedure of the "parent" packages. The registrations therein will not be made::

  >>> import grok
  >>> grok.grok('grok.tests.scan.withtestsmodules')
  >>> from zope import component
  >>> from grok.tests.scan.withtestsmodules.tests import IClub
  >>> # Test by trying to retrieve a global utility, which is not there
  >>> component.getUtility(IClub)
  Traceback (most recent call last):
  ...
  ComponentLookupError:
  (<InterfaceClass grok.tests.scan.withtestsmodules.tests.IClub>, '')

Tests and ftests modules can still be grokked when explicitely called for::

  >>> grok.grok('grok.tests.scan.withtestsmodules.tests')
  >>> from zope import component
  >>> from grok.tests.scan.withtestsmodules.tests import IClub
  >>> # Test by trying to retrieve a global utility
  >>> component.getUtility(IClub)
  <grok.tests.scan.withtestsmodules.tests.Club object at ...>
"""
