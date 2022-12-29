"""
When a GrokImportError occurs, ZCML will give the proper stack trace:

  >>> import grok
  >>> from zope.configuration import xmlconfig
  >>> context = xmlconfig.file('meta.zcml', grok)

  >>> ignored = xmlconfig.string('''
  ... <configure
  ...     xmlns="http://namespaces.zope.org/zope"
  ...     xmlns:grok="http://namespaces.zope.org/grok"
  ...     >
  ...     <grok:grok package="grok.tests.zcml.directiveerror"/>
  ... </configure>''', context=context)
  Traceback (most recent call last):
    ...
  zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "<string>", line 6.4-6.57
      martian.error.GrokError: No module-level context for <class 'grok.tests.zcml.directiveerror.CavePainting'>, please use the 'context' directive.
"""  # noqa: E501
import grok


class CavePainting(grok.View):
    pass
