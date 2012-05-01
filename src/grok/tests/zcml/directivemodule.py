"""
  >>> import grok
  >>> from zope.configuration import xmlconfig
  >>> context = xmlconfig.file('meta.zcml', grok)

  >>> ignored = xmlconfig.string('''
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:grok="http://namespaces.zope.org/grok"
  ...     >
  ...     <grok:grok package="grok.tests.zcml.stoneage.cave"/>
  ... </configure>''', context=context)

  >>> from grok.tests.zcml.stoneage.cave import Cave
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
"""
