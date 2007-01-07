"""
  >>> util.class_annotation_list(B, 'grok.foo', None)
  [7, 5]
  >>> util.class_annotation_list(B2, 'grok.foo', None)
  [5]
  >>> util.class_annotation_list(C, 'grok.foo', None)
  [8, 7, 5]
  >>> util.class_annotation_list(C2, 'grok.foo', None)
  [9, 5, 7]
  
"""
import grok
from grok import util

class A(object):
    __grok_foo__ = [5]

class B(A):
    __grok_foo__ = [7]

class B2(A):
    pass

class C(B, B2):
    __grok_foo__ = [8]

class C2(B2, B):
    __grok_foo__ = [9]
