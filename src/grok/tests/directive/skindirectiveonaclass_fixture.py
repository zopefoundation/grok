import grok

class NotAnInterfaceClass(object):
    grok.skin('failing_directive')
