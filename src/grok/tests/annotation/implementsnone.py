"""
Subclasses of grok.Annotation must implement at least one additional
interface to indicate which annotation interface they provide and can
be looked up with:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  GrokError: <class 'grok.tests.annotation.implementsnone.Branding'>
  must implement at least one interface (use grok.implements to
  specify).

"""

import grok

class Mammoth(grok.Model):
    pass

class Branding(grok.Annotation):
    pass
