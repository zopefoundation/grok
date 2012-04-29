"""
Grok allows you to set up catalog indexes in your application with a
special indexes declaration.  We do need to specify a site (such as
the application) for the Indexes however, otherwise we get a GrokError:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No site specified for grokcore.catalog.Indexes subclass in module
  <module 'grok.tests.catalog.indexes_no_app' from ...>.
  Use grokcore.site.site() to specify.

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
