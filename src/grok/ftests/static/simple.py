"""
If there is a static/ directory inside of a grokked package, its
contents will be available as static resources under a URL:

  >>> import grok
  >>> grok.grok('grok.ftests.static.simple_fixture')
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/@@/grok.ftests.static.simple_fixture/'
  ...              'file.txt')
  >>> print browser.contents
  some text

We use a special name 'static' in page templates to allow easy linking
to resources:

  >>> root = getRootFolder()
  >>> from grok.ftests.static.simple_fixture.ellie import Mammoth
  >>> root[u'ellie'] = Mammoth()
  >>> browser.open('http://localhost/ellie')
  >>> print browser.contents
  <html>
  <body>
  <a href="http://localhost/@@/grok.ftests.static.simple_fixture/file.txt">Some text in a file</a>
  </body>
  </html>

Static also means that page templates will not be interpreted:

  >>> browser.open('http://localhost/@@/grok.ftests.static.simple_fixture/static.pt')
  >>> print browser.contents
  <html>
  <body>
  <h1 tal:content="string:will not be interpreted"/>
  </body>
  </html>

We also support subdirectories for resources:

  >>> browser.open('http://localhost/@@/grok.ftests.static.simple_fixture/subdir/otherfile.txt')
  >>> print browser.contents
  This is yet another file.

Sanity check custom layers

  >>> browser.open('http://localhost/ellie/@@cavedrawings')
  >>> print browser.contents
  stick figures

  >>> browser.open('http://localhost/++skin++MammothSkin/ellie/@@tarpit')
  >>> print browser.contents
  inky darkness all around

Static layer is not available to custom layers unless they subclass IDefaultBrowserLayer

  >>> browser.open('http://localhost/++skin++MammothSkin/@@/grok.ftests.static.simple_fixture/subdir/otherfile.txt')
  Traceback (most recent call last):
  ...
  NotFound: ...

  >>> browser.open('http://localhost/++skin++Rotterdam/@@/grok.ftests.static.simple_fixture/subdir/otherfile.txt')
  >>> print browser.contents
  This is yet another file.
  
"""

