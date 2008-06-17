"""

The ordering works like so:
1. Objects with explicit ordering
   (if combined with objects with no ordering not specified, then the orderless
    objects come first)
2. Objects with same ordering get grouped by module import order
3. Internal order within module
4. If no ordering is specified by any objects, then objects are sorted
   alphabetically by class name

  >>> from inter2 import Four, Five, Six
  >>> components = [One(), Two(), Three(), Four(), Five(), Six()]

  >>> from grok.util import sort_components
  >>> sort_components(components)
  [<...Three object at ...>,
   <...One object at ...>,
   <...Five object at ...>,
   <...Six object at ...>,
   <...Four object at ...>,
   <...Two object at ...>]

"""

import grok

class One(object):
    grok.order()

class Two(object):
    grok.order(2)

class Three(object):
    pass
