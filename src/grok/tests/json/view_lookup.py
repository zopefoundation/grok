"""

The JSON grokker registers a view for each method of the JSON class.
So we should be able to search for view by method name.

  >>> grok.grok(__name__)
  >>> mammoth = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope.component import getMultiAdapter
  >>> view = getMultiAdapter((mammoth, request), name='run')

The 'run' method/view returns json data, but it looks just like python.

  >>> view()
  '{"me": "grok"}'

"""
import grok

class Mammoth(grok.Model):
    pass

class MammothView(grok.JSON):
    grok.context(Mammoth)

    def run(self):
        return { 'me': 'grok' }
