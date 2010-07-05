"""

Forms have an application_url() method to easily retrieve the url of the
application, like views does::

  >>> getRootFolder()['world'] = world = IceWorld()
  >>> world['arthur'] = Mammoth()

And we can access the display form which display the application URL::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/world/arthur')
  >>> print browser.contents
  <p> Test display: application http://localhost/world </p>

Same for the edit form::

  >>> browser.open('http://localhost/world/arthur/@@edit')
  >>> print browser.contents
  <p> Test edit: application http://localhost/world </p>


"""
import grok
from zope import schema

class IceWorld(grok.Application, grok.Container):
    pass


class Mammoth(grok.Model):
    class fields:
        name = schema.TextLine(title=u"Name")
        size = schema.TextLine(title=u"Size", default=u"Quite normal")


class Index(grok.DisplayForm):

    grok.context(Mammoth)

index = grok.PageTemplate("""
<p>
   Test display: application <tal:replace tal:replace="view/application_url" />
</p>""")


class Edit(grok.EditForm):
    
    grok.context(Mammoth)

edit = grok.PageTemplate("""
<p>
   Test edit: application <tal:replace tal:replace="view/application_url" />
</p>""")
