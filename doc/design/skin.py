import grok
from zope import interface


grok.definelayer('my')
grok.definelayer('admin')

grok.layer('my')

grok.defineskin('my', ['my'])         # this is the default
grok.defineskin('my')                 # does the same as the line above
grok.defineskin('admin', ['admin', 'my'])


class Painting(grok.View):
    pass


fireplace = grok.PageTemplate("""\
<html><body></body></html>
""")


class AdminPainting(grok.View):
    grok.layer('adminlayer')
