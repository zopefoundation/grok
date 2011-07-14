"""
Demonstrate the grokcore.chameleon template component has been registered.


  >>> from zope.app.wsgi.testlayer import Browser
  >>> getRootFolder()["mammoth"] = Mammoth()
  >>> browser = Browser()
  >>> browser.open("http://localhost/mammoth/@@index")
  >>> print browser.contents
  <html>Mammoth</html>

"""
import grok

grok.templatedir('templates')

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    grok.context(Mammoth)
    grok.template('available')
