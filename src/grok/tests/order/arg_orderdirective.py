"""

If the grok.order directive is present with arguments, sorting will be
done by the order specified.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grok.util import sort_components
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...Fourth object at ...>,
   <...Third object at ...>,
   <...Second object at ...>,
   <...First object at ...>]

"""

import grok

class First(object):
    grok.order(5)

class Second(object):
    grok.order(4)

class Third(object):
    grok.order(3)

class Fourth(object):
    grok.order(2)

class Fifth(object):
    grok.order(1)
