"""

If the grok.order directive is present with no arguments, sorting will
be done by definition order.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grok.util import sort_components
  >>> sort_components(components)
  [<...First object at ...>,
   <...Second object at ...>,
   <...Third object at ...>,
   <...Fourth object at ...>,
   <...Fifth object at ...>]

"""

import grok

class First(object):
    grok.order()

class Second(object):
    grok.order()

class Third(object):
    grok.order()

class Fourth(object):
    grok.order()

class Fifth(object):
    grok.order()
