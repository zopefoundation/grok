"""
If there is a static/ directory inside of a grokked package, its
contents will be available as static resources under a URL:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/@@/grok.ftests.staticdir.simple_fixture/'
  ...              'file.txt')
  >>> print browser.contents
  some text

We use a special name 'static' in page templates to allow easy linking
to resources:

  >>> root = getRootFolder()
  >>> from grok.ftests.staticdir.simple_fixture.ellie import Mammoth
  >>> root[u'ellie'] = Mammoth()
  >>> browser.open('http://localhost/ellie')
  >>> print browser.contents
  <html>
  <body>
  <a href="http://localhost/@@/grok.ftests.staticdir.simple_fixture/file.txt">Some text in a file</a>
  </body>
  </html>

Static also means that page templates will not be interpreted:

  >>> browser.open('http://localhost/@@/grok.ftests.staticdir.simple_fixture/static.pt')
  >>> print browser.contents
  <html>
  <body>
  <h1 tal:content="string:will not be interpreted"/>
  </body>
  </html>

We also support subdirectories for resources:

  >>> browser.open('http://localhost/@@/grok.ftests.staticdir.simple_fixture/subdir/otherfile.txt')
  >>> print browser.contents
  This is yet another file.

"""
