"""
  >>> import grok.scan

If you call grok.scan.modules() on a module, it yields the module name:

  >>> from grok.tests.scan.stoneage import cave
  >>> list(grok.scan.modules('grok.tests.scan.stoneage.cave', cave.__file__))
  ['grok.tests.scan.stoneage.cave']

If you call it on a package, it yield a list of the names of the
package, its modules, and all its subpackages and their modules.

  >>> from grok.tests.scan import stoneage
  >>> list(grok.scan.modules('grok.tests.scan.stoneage', stoneage.__file__))
  ['grok.tests.scan.stoneage', 'grok.tests.scan.stoneage.cave',
  'grok.tests.scan.stoneage.hunt', 'grok.tests.scan.stoneage.hunt.mammoth',
  'grok.tests.scan.stoneage.painting']
  
"""
