"""

If the grok.order directive is specified with other classes that don't
have the order specified, then the order will be determined by first
sorting on the order specified, and then by the definition order.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grok.util import sort_components
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...Third object at ...>,
   <...First object at ...>,
   <...Fourth object at ...>,
   <...Second object at ...>]

"""

import grok

class First(object):
    grok.order()

class Second(object):
    grok.order(1)

class Third(object):
    pass

class Fourth(object):
    grok.order()

class Fifth(object):
    pass
