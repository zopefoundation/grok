"""
It is too confusing to have a template that would be implicitly
associated with a view while that view already refers to another
template using grok.template.  Therefore there is an error:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Multiple possible templates for view
  <class 'grok.tests.view.explicitimplicittemplate.Painting'>.
  It uses grok.template('cavepainting'), but there is also a template
  called 'painting'.

"""
import grok

class Mammoth(grok.Model):
    pass

class Painting(grok.View):
    grok.template('cavepainting')

cavepainting = grok.PageTemplate("GROK CAVEPAINT MAMMOTH!")
painting = grok.PageTemplate("GROK PAINT MAMMOTH!")
