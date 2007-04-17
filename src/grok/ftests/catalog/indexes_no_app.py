"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration.  We do need to specify an application for
the Indexes however, otherwise we get a GrokError:

  >>> import grok
  >>> grok.grok('grok.ftests.catalog.indexes_no_app')
  Traceback (most recent call last):
    ...
  GrokError: No application specified for grok.Indexes subclass in module
  <module 'grok.ftests.catalog.indexes_no_app' from ...>.
  Use grok.application() to specify.
  
"""
import grok
from grok import index

class Herd(grok.Container, grok.Application):
    pass

class Mammoth(grok.Model):
    pass

class MammothIndexes(grok.Indexes):
    grok.context(Mammoth)
    grok.name('foo_catalog')
    
    name = index.Field()
    age = index.Field()
    message = index.Text()
