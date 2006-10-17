"""
A View may either have an associated template or a render-method. Here
we check that this also works for templates in a template-directory:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible ways to render view
  <class 'grok.tests.view.dirtemplateandrender.CavePainting'>.
  It has both a 'render' method as well as an associated template.

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    def render(self):
        pass
