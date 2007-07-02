"""
  >>> import grok
  >>> from megrok.view.tests.view.macros import Mammoth
  >>> grok.grok('megrok.view.tests.view.macros')
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred/@@painting")
  >>> print browser.contents
  <html>
  <body>
  <h1>GROK MACRO!</h1>
  <div>
  GROK SLOT!
  </div>
  </body>
  </html>

Views without a template do not support macros:

  >>> browser.open("http://localhost/manfred/@@dancing")
  Traceback (most recent call last):
  AttributeError: 'DancingHall' object has no attribute 'template'

If the view has an attribute with the same name as a macro, the macro 
shadows the view. XXX This should probably generate a warning at runtime.

  >>> browser.open("http://localhost/manfred/@@grilldish")
  >>> print browser.contents
  <html>
  Curry
  </html>

"""
import grok
import megrok.view

class Mammoth(grok.Model):
    pass

class DancingHall(megrok.view.View):

    def render(self):
        return "A nice large dancing hall for mammoths."

class Grilled(megrok.view.View):

    def update(self):
        self.spices = "Pepper and salt"

class Painting(megrok.view.View):
    pass

painting = grok.PageTemplate("""\
<html metal:use-macro="context/@@layout/main">
<div metal:fill-slot="slot">
GROK SLOT!
</div>
</html>
""")

class Layout(megrok.view.View):
    pass

layout = grok.PageTemplate("""\
<html metal:define-macro="main">
<body>
<h1>GROK MACRO!</h1>
<div metal:define-slot="slot">
</div>
</body>
</html>""")

class Dancing(megrok.view.View):
    pass

dancing = grok.PageTemplate("""\
<html metal:use-macro="context/@@dancinghall/something">
</html>
""")

class GrillDish(megrok.view.View):
    pass

grilldish = grok.PageTemplate("""
<html metal:use-macro="context/@@grilled/spices">
</html>""")

class Grilled(megrok.view.View):
    pass

grilled = grok.PageTemplate("""\
<html metal:define-macro="spices">
Curry
</html>""")
