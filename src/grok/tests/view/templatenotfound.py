"""
This should fail because ``grok.template`` points to a non-existing
template:

  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: View <class 'grok.tests.view.templatenotfound.Painting'>
  has no associated template or 'render' method.

"""
import grok

class Mammoth(grok.Model):
    pass

class Painting(grok.View):
    grok.template('cavepainting')

# no cavepainting template here
