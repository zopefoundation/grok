"""

If the grok.order directive is absent, sorting will be done by class
name.

  >>> components = [First(), Second(), Third(), Fourth(), Fifth()]

  >>> from grok.util import sort_components
  >>> sort_components(components)
  [<...Fifth object at ...>,
   <...First object at ...>,
   <...Fourth object at ...>,
   <...Second object at ...>,
   <...Third object at ...>]

"""

class First(object):
    pass

class Second(object):
    pass

class Third(object):
    pass

class Fourth(object):
    pass

class Fifth(object):
    pass
