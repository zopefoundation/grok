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
  ...     <grok:grok package="grok.tests.zcml.directiveimporterror_fixture"/>
  ... </configure>''', context=context)
  Traceback (most recent call last):
    ...
  ZopeXMLConfigurationError: File "...", line ...
  GrokImportError: The 'template' directive can only be used on class level.
"""
