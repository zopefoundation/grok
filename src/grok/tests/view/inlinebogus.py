# -*- coding: latin-1 -*-
"""
We do not accept bogus inline template such as ones that contain
encoded strings:

  >>> import grok
  >>> grok.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Invalid inline template 'cavepainting_pt' for <class 'grok.tests.view.inlinebogus.CavePainting'>. Inline templates must be unicode or ASCII.

"""
import grok

class Mammoth(grok.Model):
    pass

class CavePainting(grok.View):
    pass

cavepainting_pt = """\
<html>
<body><h1 tal:content="string:Mammoth Cave Painting"/>
<p>ööö</p>
</body>
</html>
"""
