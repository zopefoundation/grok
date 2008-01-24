# -*- coding: latin-1 -*-
"""
You can only pass unicode to `grok.name`:

  >>> pass_unicode()
  >>> pass_encodedstring()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass unicode or ASCII to grok.name.
  >>> pass_object()
  Traceback (most recent call last):
    ...
  GrokImportError: You can only pass unicode or ASCII to grok.name.

"""
import grok

def pass_unicode():
    class View(object):
        grok.name(u'name')

def pass_encodedstring():
    class View(object):
        grok.name("ölkj")

def pass_object():
    class View(object):
        grok.name(object())
