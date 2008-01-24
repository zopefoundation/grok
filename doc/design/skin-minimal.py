import grok
from zope import interface


grok.definelayer('my')
grok.defineskin('my')                 # Picks up the layer 'my' if it exists

grok.layer('my')                      # If there is only a single layer defined
                                      # in a module, it will be the default


class Painting(grok.View):
    pass


fireplace = grok.PageTemplate("""\
<html><body></body></html>
""")
