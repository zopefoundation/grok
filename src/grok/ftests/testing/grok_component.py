"""
Test grok_component().

grok.testing.grok_component() can be used to grok individual
components within a doctest, such as adapters. It sets up just enough
context for some grokking to work, though more complicated grokkers
which need module context (such as view grokkers) might not work.

This defines the object we want to provide an adapter for::

  >>> class Bar(object):
  ...    pass

This is the interface that we want to adapt to::

  >>> from zope.interface import Interface
  >>> class IFoo(Interface):
  ...    pass

This is the adapter itself::

  >>> import grok
  >>> class MyAdapter(grok.Adapter):
  ...    grok.provides(IFoo)
  ...    grok.context(Bar)

Now we will register the adapter using grok_component()::

  >>> from grok.testing import grok_component
  >>> grok_component('MyAdapter', MyAdapter)
  True
  
The adapter should now be available::

  >>> adapted = IFoo(Bar())
  >>> isinstance(adapted, MyAdapter)
  True
"""
