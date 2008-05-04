"""
This module used by inter1 tests
"""

import grok

class Four(object):
    grok.order(1)

class Five(object):
    pass

class Six(object):
    grok.order()
