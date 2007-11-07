"""

We expect this grok to fail, and give 

  >>> try:
  ...     grok.testing.grok(__name__)
  ... except ConfigurationExecutionError, error:
  ...     pass
  >>> error.evalue.component
  <class 'grok.tests.error.error.CavePainting'>

"""

import grok
from zope.configuration.config import ConfigurationExecutionError

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    grok.template("a")

a = grok.PageTemplate("a")
cavepainting = grok.PageTemplate("b")
