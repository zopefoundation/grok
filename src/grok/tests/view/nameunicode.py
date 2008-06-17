# -*- coding: latin-1 -*-
"""
You can only pass unicode to `grok.name`:

  >>> pass_unicode()
  >>> pass_encodedstring()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'name' directive can only be called with
  unicode or ASCII.

  >>> pass_object()
  Traceback (most recent call last):
    ...
  GrokImportError: The 'name' directive can only be called with
  unicode or ASCII.

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
