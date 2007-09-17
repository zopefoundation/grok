"""
  >>> util.class_annotation_list(B, 'grok.foo', None)
  [5, 7]
  >>> util.class_annotation_list(B2, 'grok.foo', None)
  [5]
  >>> util.class_annotation_list(C, 'grok.foo', None)
  [5, 7, 8]
  >>> util.class_annotation_list(C2, 'grok.foo', None)
  [5, 7, 9]

"""
import grok
from martian import util

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
