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
  ME GROK STILL SEE BEAR NAMED Bjorn!

"""
import grok
import martian
import os.path

class PercentTemplate(object):
    """A simple template class that does Python %-substitution."""
    def __init__(self, text):
        self.text = text

    def render(self, **namespace):
        return self.text % namespace

class PercentPageTemplate(grok.components.GrokTemplate):
    """Glue class suggested by doc/minitutorials/template-languages.txt."""

    def fromTemplate(self, template):
        return PercentTemplate(template)

    def fromFile(self, filename, _prefix=None):
        file = open(os.path.join(_prefix, filename))
        return PercentTemplate(file.read())

    def render(self, view):
        return self.getTemplate().render(**self.getNamespace(view))

class PercentPageTemplateFileFactory(grok.GlobalUtility):
    """Glue class suggested by doc/minitutorials/template-languages.txt."""
    
    grok.implements(grok.interfaces.ITemplateFileFactory)
    grok.name('pct')

    def __call__(self, filename, _prefix=None):
        return PercentPageTemplate(filename=filename, _prefix=_prefix)


class Bear(grok.Model):
    def __init__(self, name):
        self.name = name

class Index(grok.View):
    def namespace(self):
        return { 'bear_name': self.context.name }

index = PercentPageTemplate(filename='language_file.txt',
                            _prefix=os.path.dirname(__file__))
