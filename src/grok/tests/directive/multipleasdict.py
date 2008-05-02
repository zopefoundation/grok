"""
The MultipleTimesAsDictDirective is used by grok.traversable so multiple
attributes can be mentioned.

  >>> from martian import scan
  >>> from grok.tests.directive import multipleasdict
  >>> module_info = scan.module_info_from_module(multipleasdict)

  >>> g = Club.__grok_traversable__
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
