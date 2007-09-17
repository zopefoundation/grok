"""
Filesystem-based templates, once grokked, can be changed.  The change
will automatically be picked up, reloading Zope is not necessary.

  >>> grok.grok(__name__)
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = getMultiAdapter((Mammoth(), request), name='index')
  >>> print view()
  before

Now we change the file:

  >>> import os.path
  >>> here = os.path.dirname(__file__)
  >>> template_file = os.path.join(here, 'templatereload_templates', 'index.pt')
  >>> template = open(template_file, 'w')
  >>> template.write('after')
  >>> template.close()

and find that the output of the view has changed as well:

  >>> print view()
  after

At last, we should change everything back to normal:

  >>> template = open(template_file, 'w')
  >>> template.write('before')
  >>> template.close()
"""
import grok

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    pass
