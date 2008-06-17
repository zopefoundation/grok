"""
The MultipleTimesAsDictDirective is used by grok.traversable so multiple
attributes can be mentioned.

  >>> from martian import scan
  >>> import grok
  >>> g = grok.traversable.bind().get(Club)
  >>> isinstance(g, dict)
  True
  >>> g['demo']
  'demo'
  >>> g['attr']
  'attr'
  >>> g['asdf']
  'attr'
"""
import grok
from zope import interface

class Club(grok.Model):
    grok.traversable('asdf', name='attr')
    grok.traversable('attr')
    grok.traversable('attr', name='asdf')
    grok.traversable('demo')
    demo = 'something'
