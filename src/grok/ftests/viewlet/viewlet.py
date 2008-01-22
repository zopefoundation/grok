"""

Test Viewlets
=============

    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()
    >>> betty = CaveWoman()
    >>> view = CaveView(betty, request)
    >>> print view()
    Brack Bone
    T-Rex Bone
    <BLANKLINE>
"""


import grok


class CaveWoman(grok.Model):
    pass


class Template(grok.View):
    pass


template = grok.PageTemplateFile('viewlet.pt')
template.__grok_name__ = 'testtemplate'
template.__grok_location__ = None

class CaveView(grok.View):
    template = template
    def render(self):
        pass

class Pot(grok.ViewletManager):
    grok.context(CaveView)
    grok.name('pot') # default


class TRexBone(grok.Viewlet):
    grok.viewletmanager(Pot)

    def render(self):
        return "T-Rex Bone"


class BrackerBone(grok.Viewlet):
    grok.viewletmanager(Pot)

    def render(self):
        return "Brack Bone"
