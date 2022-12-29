"""
Subclasses of grok.GlobalUtility that implement more than one interface must
specify which interface to use for the registration:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  martian.error.GrokError: <class 'grok.tests.utility.implementsmany2.Club'> is implementing more than one interface (use grok.provides to specify which one to use).
"""  # noqa: E501
from zope import interface

import grok


class IClub(interface.Interface):
    pass


class ISpikyClub(interface.Interface):
    pass


@grok.implementer(IClub, ISpikyClub)
class Club:
    pass


grok.global_utility(Club)
