from zope.interface import Interface
import grok

class IClub(Interface):
    pass

class Club(grok.GlobalUtility):
    grok.provides(IClub)

import unittest
def test_suite():
    return unittest.TestSuite() # return an empty suite
