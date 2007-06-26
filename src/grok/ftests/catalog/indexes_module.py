"""
You can create an index on module level, but that should lead to a GrokError:

  >>> import grok
  >>> from grok.ftests.catalog.indexes_module import func
  >>> func()
  Traceback (most recent call last):
    ...
  GrokImportError: <class 'grok.index.Field'> can only be instantiated on
  class level.
"""
from grok import index

def func():
    foo = index.Field()
    
