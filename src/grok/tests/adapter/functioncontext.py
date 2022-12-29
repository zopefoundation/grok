"""
You can't call grok.context from a function:

  >>> func()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be used on class or module level.

You can't call grok.context from a method either:

  >>> SomeClass().meth()
  Traceback (most recent call last):
    ...
  martian.error.GrokImportError: The 'context' directive can only be used on class or module level.
"""  # noqa: E501
import grok
from grok.tests.adapter.adapter import Cave


def func():
    """We don't allow calling `grok.context` from anything else than a
    module or a class"""
    grok.context(Cave)


class SomeClass:

    def meth(self):
        """We don't allow calling `grok.context` from anything else
        than a module or a class"""
        grok.context(Cave)
