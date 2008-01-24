"""
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
  
You can skip the "macro" part of the macro call, but this is deprecated:

  >>> from zope.deprecation.tests import warn
  >>> import warnings
  >>> saved_warn = warnings.warn
  >>> warnings.warn = warn

  >>> browser.open("http://localhost/manfred/@@burnt")
  From tests.py's showwarning():
  ... DeprecationWarning: Calling macros directly on the view is deprecated. Please use context/@@viewname/macros/macroname
  ...
  
  >>> warnings.warn = saved_warn

"""
import grok

class Mammoth(grok.Model):
    pass

class DancingHall(grok.View):

    def render(self):
        return "A nice large dancing hall for mammoths."

class Grilled(grok.View):

    def update(self):
        self.spices = "Pepper and salt"

class Painting(grok.View):
    pass

painting = grok.PageTemplate("""\
<html metal:use-macro="context/@@layout/macros/main">
<div metal:fill-slot="slot">
GROK SLOT!
</div>
</html>
""")

class Layout(grok.View):
    pass

layout = grok.PageTemplate("""\
<html metal:define-macro="main">
<body>
<h1>GROK MACRO!</h1>
<div metal:define-slot="slot">
</div>
</body>
</html>""")

class Dancing(grok.View):
    pass

dancing = grok.PageTemplate("""\
<html metal:use-macro="context/@@dancinghall/macros/something">
</html>
""")

class GrillDish(grok.View):
    pass

grilldish = grok.PageTemplate("""
<html metal:use-macro="context/@@grilled/macros/spices">
</html>""")

class Burnt(grok.View):
    pass

burnt = grok.PageTemplate("""\
<html metal:use-macro="context/@@grilled/spices">
</html>""")

class Grilled(grok.View):
    pass

grilled = grok.PageTemplate("""\
<html metal:define-macro="spices">
Curry
</html>""")

