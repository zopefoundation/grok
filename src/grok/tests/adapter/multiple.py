"""
Multiple models lead to ambiguity:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: Multiple possible contexts for <class 'grok.tests.adapter.multiple.Home'>, please use the 'context' directive.

"""  # noqa: E501
import grok
from zope import interface


class Cave(grok.Model):
    pass


class Club(grok.Model):
    pass


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
