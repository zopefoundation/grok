"""

We expect this grok to fail, and give

  >>> error_component = None
  >>> try:
  ...     grok.testing.grok(__name__)
  ... except ConfigurationExecutionError as error:
  ...     if sys.version_info[0] >= 3:
  ...         error_component = error.args[1].component
  ...     else:
  ...         error_component = error.evalue.component
  >>> error_component
  <class 'grok.tests.error.error.CavePainting'>

"""

import grok
import sys
from zope.configuration.config import ConfigurationExecutionError

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    grok.template("a")

a = grok.PageTemplate("a")
cavepainting = grok.PageTemplate("b")
