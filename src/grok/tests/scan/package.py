"""
  >>> import grok
  >>> grok.grok('grok.tests.scan.stoneage')

  >>> from grok.tests.scan.stoneage.cave import Cave
  >>> from grok.tests.scan.stoneage.hunt.mammoth import Mammoth
  >>> manfred = Mammoth()
  >>> cave = Cave()
  
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component

  >>> view = component.getMultiAdapter((cave, request), name='index')
  >>> print view()
  <html>
  <body>
  <h1>A comfy cave</h1>
  </body>
  </html>
  
  >>> view = component.getMultiAdapter((manfred, request), name='index')
  >>> print view()
  <html>
  <body>
  <h1>ME GROK HUNT MAMMOTH!</h1>
  </body>
  </html>
"""
