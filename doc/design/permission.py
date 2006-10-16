import grok

grok.definepermission('grok.Complex')  # define permission first

class Complex(grok.Model):
    # this sets the default for all methods
    grok.require('zope.Public')  # this is actually the default

    # this sets the default for reading all attributes that are not methods
    grok.readable('zope.Public')  # this is actually the default

    # this sets the default for writing all attributes that are not methods
    grok.writable('zope.Public')  # this is actually the default

    # this overrides the above
    grok.readable('grok.Complex', 'attr1') # override default
    grok.readable('zope.ManageServices', 'attr2') # override default
    grok.writable('zope.ManageContent', 'attr1', 'attr2') # override default

    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2

    @grok.require('some.permission')
    def doSomethingVerySecret(self):
        pass

    @grok.require('zope.Public')  # this is actually the default
    def imPublic(self):
        pass

class SubClass(Complex):
    # it's all inherited

    grok.readable('zope.Public', 'attr1')

