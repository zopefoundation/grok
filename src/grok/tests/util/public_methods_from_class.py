"""
  >>> methods = grok.util.public_methods_from_class(A)
  >>> sorted([m.__name__ for m in methods])
  ['should_also_be_public', 'should_be_public']

"""
import grok
import grok.util

class A(object):

    def __init__(self):
        pass # this method is ignored

    def __call__(self):
        pass # this method is ignored

    def __double_underscored(self):
        pass # this method is ignored

    def _single_underscored(self):
        pass # this method is ignored

    def should_be_public(self):
        pass # this method is found

    def should_also_be_public(self):
        pass # this method is found
