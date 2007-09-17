"""

We expect this grok to fail, and give 

  >>> try:
  ...     grok.grok(__name__)
  ... except grok.GrokError, error:
  ...     pass
  >>> error.component
  <class 'grok.tests.error.error.CavePainting'>

"""

import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    grok.template("a")

a = grok.PageTemplate("a")
cavepainting = grok.PageTemplate("b")
