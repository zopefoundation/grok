"""
Demonstrate the grokcore.chameleon template component has been registered.


  >>> from zope.testbrowser.wsgi import Browser
  >>> getRootFolder()["mammoth"] = Mammoth()
  >>> browser = Browser(wsgi_app=wsgi_app())
  >>> browser.open("http://localhost/mammoth/@@index")
  >>> print(browser.contents)
  <html>Mammoth</html>

"""
import grok

grok.templatedir('templates')

class Mammoth(grok.Model):
    pass

class Index(grok.View):
    grok.context(Mammoth)
    grok.template('available')
