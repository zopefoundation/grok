"""
Subclasses of grok.Adapter and grok.MultiAdapter must implement exactly one
interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: <class 'grok.tests.adapter.implementsnonemulti.Home'> must implement at least one interface (use grok.implements to specify).
"""  # noqa: E501
import grok


class Cave(grok.Model):
    pass


class Home(grok.MultiAdapter):
    pass
