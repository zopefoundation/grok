"""
  >>> getRootFolder()['cave'] = cave = Cave()

JSON views answer a special content-type::

  >>> print http('GET /cave/show HTTP/1.1')
  HTTP/1. 200 Ok
  Content-Length: 17
  Content-Type: application/json
  <BLANKLINE>
  "A Cavemans cave"

"""

import grok

class Cave(grok.Model):
    pass

class CaveJSON(grok.JSON):
    def show(self):
        return 'A Cavemans cave'