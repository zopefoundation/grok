import grok
from zope import interface


grok.definelayer('my')
grok.definelayer('admin')

grok.layer('my')

grok.skin('my', ['my'])         # this is the default
grok.skin('my')                 # does the same as the line above
grok.skin('admin', ['admin', 'my'])


class Painting(grok.View):
    pass


fireplace = grok.PageTemplate("""\
<html><body></body></html>
""")


class AdminPainting(grok.View):
    grok.layer('adminlayer')
