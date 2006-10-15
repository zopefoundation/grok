"""
Templates can be specified in the same module as the view,
using a variable named `viewname_pt`:

  >>> grok.grok(__name__)
  
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
"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass

cavepainting_pt = """\
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
"""
