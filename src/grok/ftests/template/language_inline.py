"""
Containers can determine how they want to be traversed by
implementing a 'traverse' method, but the behavior falls back to
basic container traversal if the 'traverse' method returns None:

  >>> getRootFolder()["bear"] = Bear('Bjorn')

Let's first try to look up the special traversed item:

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/bear")
  >>> print browser.contents
  ME GROK SEE BEAR NAMED Bjorn!

"""
import grok
import martian

class PercentTemplate(object):
    """A simple template class that does Python %-substitution."""
    def __init__(self, text):
        self.text = text

    def render(self, **namespace):
        return self.text % namespace

class PercentPageTemplate(grok.components.GrokPageTemplate):
    """Glue class suggested by doc/minitutorials/template-languages.txt."""
    def __init__(self, html):
        self._template = PercentTemplate(html)
        self.__grok_module__ = martian.util.caller_module()

    def _initFactory(self, factory):
        pass
    
    def namespace(self, view):
        namespace = {}
        namespace['request'] = view.request
        namespace['view'] = view
        namespace['context'] = view.context
        namespace['static'] = view.static
        return namespace
    
    def render(self, view):
        namespace = self.namespace(view)
        namespace.update(view.namespace())        
        return self._template.render(**namespace)

class Bear(grok.Model):
    def __init__(self, name):
        self.name = name

class Index(grok.View):
    def namespace(self):
        return { 'bear_name': self.context.name }

index = PercentPageTemplate(
    "ME GROK SEE BEAR NAMED %(bear_name)s!"
    )
