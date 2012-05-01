"""
  >>> import grok
  >>> from zope.configuration import xmlconfig

  >>> ignored = xmlconfig.string('''
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:grok="http://namespaces.zope.org/grok"
  ...     >
  ...     <include package="grok" file="meta.zcml" />
  ...     <grok:grok package="grokcore.view.templatereg" />
  ...     <grok:grok package="grok.tests.zcml.stoneage"/>
  ... </configure>''')

  >>> from grok.tests.zcml.stoneage.cave import Cave
  >>> from grok.tests.zcml.stoneage.hunt.mammoth import Mammoth
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
