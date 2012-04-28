"""
You can create an index on module level, but that should lead to a GrokError:

  >>> func()
  Traceback (most recent call last):
    ...
  GrokImportError: <class 'grokcore.catalog.index.Field'> can only be instantiated on
  class level.
"""
from grok import index

def func():
    foo = index.Field()
    
