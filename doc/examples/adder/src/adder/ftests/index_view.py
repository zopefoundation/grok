"""
The Index view of the Adder app has a form for entering items to be added

  >>> from adder.app import Adder
  >>> getRootFolder()['adder'] = adder = Adder()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.open('http://localhost/adder')

Since we've just started the Adder, there shouldn't be a "Clear" button

  >>> browser.getControl('bt_clear')
  Traceback (innermost last):
  ...
  LookupError: name 'bt_clear'
  
There should be an entry field for the number to be added
and a "+" button.

  >>> browser.getControl('term').value = '1.234'
  >>> browser.getControl('bt_add').value
  '+'
  >>> browser.getControl('bt_add').click()

We should find the '1.234' value twice: one in the total, one in the "tape"

    >>> browser.contents.count('1.234')
    2

We can add another number:
  
    >>> browser.getControl('term').value = '2'
    >>> browser.getControl('bt_add').click()

And see the total and the "tape" numbers:

    >>> '3.234' in browser.contents
    True
    >>> '1.234' in browser.contents
    True
    >>> '2.0' in browser.contents
    True

Also, now that we have some numbers in the "tape", there should be a "Clear"
button, which clears the tape and the total:

    >>> browser.getControl('bt_clear').click()
    >>> '3.234' in browser.contents
    False

"""
