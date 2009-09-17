"""
We make sure we indeed have a view for BoneBag; this way we know it's
registered as the default context object:


    >>> grok.testing.grok(__name__)
    >>> bag = BoneBag()
    >>> from zope import component
    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()
    >>> view = component.getMultiAdapter((bag, request), name='index')
    >>> view()
    'Hello world'
"""
import grok

class BoneBag(grok.Container):
    pass

class Index(grok.View):
    """A simple view to test whether BoneBag is really registered as a model.
    """
    def render(self):
        return "Hello world"
