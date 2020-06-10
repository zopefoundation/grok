"""
Subclasses of grok.MultiAdapter must declare what they adapt,
using grok.adapts:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: <class 'grok.tests.adapter.multiadaptsnone.Home'>
  must specify which contexts it adapts
  (use the 'adapts' directive to specify).
"""
import grok

from zope import interface


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.MultiAdapter):
    pass
