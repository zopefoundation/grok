"""
You can't use @grok.traverse more than once on a class:

  >>> using_traverse_twice()
  Traceback (most recent call last):
   ...
  GrokImportError: @grok.traverse can only be used once per class.

You can't use @grok.traverse outside a class definition:

  >>> outside_class()
  Traceback (most recent call last):
   ...
  GrokImportError: @grok.traverse can only be used on class level.


"""
import grok

def using_traverse_twice():
    class Herd(grok.Model):

        @grok.traverse
        def getMammoth(self, name):
            pass

        @grok.traverse
        def getAntilope(self, name):
            pass

def outside_class():

    @grok.traverse
    def getMammoth(self, name):
        pass
