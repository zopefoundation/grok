"""

  >>> from grok.scan import ModuleInfo, module_info_from_dotted_name
  
  >>> module_info = module_info_from_dotted_name('grok.tests.scan.stoneage')
  >>> module_info
  <ModuleInfo object for 'grok.tests.scan.stoneage'>
  >>> module_info.isPackage()
  True
  >>> module_info.dotted_name
  'grok.tests.scan.stoneage'
  >>> module_info.name
  'stoneage'

  >>> module = module_info.getModule()
  >>> module
  <module 'grok.tests.scan.stoneage' from '...__init__.py...'>

  >>> module.__grok_foobar__ = 'GROK LOVE FOO'
  >>> module_info.getAnnotation('grok.foobar', None)
  'GROK LOVE FOO'
  >>> module_info.getAnnotation('grok.barfoo', 42)
  42

  >>> sub_modules = module_info.getSubModuleInfos()
  >>> sub_modules
  [<ModuleInfo object for 'grok.tests.scan.stoneage.cave'>,
   <ModuleInfo object for 'grok.tests.scan.stoneage.hunt'>,
   <ModuleInfo object for 'grok.tests.scan.stoneage.painting'>]
  >>> cave_module_info = sub_modules[0]

Module-level specifics
----------------------

cave is a module, not a package.

  >>> cave_module_info.isPackage()
  False
  >>> cave_module_info.dotted_name
  'grok.tests.scan.stoneage.cave'
  >>> cave_module_info.name
  'cave'
  >>> cave_module_info.getSubModuleInfos()
  []

Resource paths
--------------

For packages, a resource path will be a child of the package directory:

  >>> import os.path
  >>> expected_resource_path = os.path.join(os.path.dirname(
  ...     module.__file__), 'stoneage-templates')
  >>> resource_path = module_info.getResourcePath('stoneage-templates')
  >>> resource_path == expected_resource_path
  True

For modules, a resource path will be a sibling of the module's file:

  >>> expected_resource_path = os.path.join(os.path.dirname(
  ...     cave_module_info.getModule().__file__), 'cave-templates')
  >>> resource_path = cave_module_info.getResourcePath('cave-templates')
  >>> resource_path == expected_resource_path
  True

"""
