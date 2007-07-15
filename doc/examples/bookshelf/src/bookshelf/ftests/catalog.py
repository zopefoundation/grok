"""
Some simple tests, just for test the tests. :-)

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/')
  >>> browser.getControl('Application').displayValue = ['bookshelf.app.BookShelf']
  >>> browser.getControl('Name').value = 'bookshelf'
  >>> browser.getControl('Add').click()
  >>> browser.getLink('bookshelf').click()
  >>> print browser.contents
  <html>
  ...
      <ul>
          <li><a href="http://localhost/bookshelf/shelf">catalog</a></li>
      </ul>
  ...
  >>> root = getRootFolder()
  >>> bookshelf = root['bookshelf']
  >>> for k in bookshelf.keys(): print k
  shelf

"""
