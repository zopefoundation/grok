"""
We expect this grok to fail, and give

  >>> from zope.configuration.config import ConfigurationExecutionError
  >>> error_component = None
  >>> try:
  ...     grok.testing.grok(__name__)
  ... except ConfigurationExecutionError as error:
  ...     error_component = error.evalue.component
  >>> error_component
  <class 'grok.tests.error.error.CavePainting'>
"""

import grok


class Mammoth(grok.Model):
    pass


class CavePainting(grok.View):
    grok.template("a")


a = grok.PageTemplate("a")
cavepainting = grok.PageTemplate("b")
