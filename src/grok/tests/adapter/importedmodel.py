"""
Imported model and adapter won't be grokked:

  >>> import grok
  >>> grok.testing.grok(__name__)
  >>> from grok.tests.adapter.adapter import IHome
  >>> cave = Cave()
  >>> home = IHome(cave)
  Traceback (most recent call last):
    ...
  TypeError: ('Could not adapt', <grok.tests.adapter.adapter.Cave object at ...>, <InterfaceClass grok.tests.adapter.adapter.IHome>)

"""
from grok.tests.adapter.adapter import Cave, Home
