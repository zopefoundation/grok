"""
If there is a static/ directory inside of a grokked package, its
contents will be available as static resources under a URL:

  >>> grok.grok('grok.tests.static.simple_fixture')
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/++resource++grok.tests.static.simple_fixture/file.txt')
  >>> print browser.contents
  some text
"""
import grok

# class Mammoth(grok.Model):
#     pass

# index = grok.PageTemplate("""\
# <html>
# <body>
# <h1 tal
