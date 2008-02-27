"""
Templates can be specified in the same module as the view,
using a variable named `viewname_pt`:

  >>> grok.testing.grok(__name__)
  
  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> print view()
  <html>
  <body>
  <h1>Mammoth Cave Painting</h1>
  <ul>
    <li><zope.publisher.browser.TestRequest instance URL=http://127.0.0.1></li>
    <li><grok.tests.view.inline.CavePainting object at 0x...></li>
    <li><grok.tests.view.inline.Mammoth object at 0x...></li>
    <li><zope.app.pagetemplate.engine.TraversableModuleImporter object at 0x...></li>
  </ul>
  </body>
  </html>

Note that the CavePainting instance is bound to the ``view`` name in
the template.  This shows that the association of inline PageTemplate
and the view class is successful.

Finding a template does not depend on the view name, but on the class
name:

  >>> view = component.getMultiAdapter((manfred, request), name='hunting')
  >>> print view()
  <html><body><h1>GROK HUNT MAMMOTH!</h1></body></html>

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass

cavepainting = grok.PageTemplate("""\
<html>
<body>
<h1 tal:content="string:Mammoth Cave Painting"/>
<ul>
  <li tal:content="structure python:repr(request)" />
  <li tal:content="structure nocall:view" />
  <li tal:content="structure nocall:context" />
  <li tal:content="structure nocall:modules" />
</ul>
</body>
</html>
""")

class Hunt(grok.View):
    grok.name('hunting')

hunt = grok.PageTemplate("""\
<html><body><h1>GROK HUNT MAMMOTH!</h1></body></html>
""")

