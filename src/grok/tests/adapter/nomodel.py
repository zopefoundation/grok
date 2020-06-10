"""
If no model can be found in the module, we get an error:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: No module-level context for <class 'grok.tests.adapter.nomodel.Home'>, please use the 'context' directive.

"""  # noqa: E501
import grok
from zope import interface


class IHome(interface.Interface):
    pass


@grok.implementer(IHome)
class Home(grok.Adapter):
    pass
