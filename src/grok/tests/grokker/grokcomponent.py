"""

Let's first grok the meta module to define some basic grokkers::

  >>> import grok

It is possible to grok an individual component. Let's define an adapter::

  >>> from zope.interface import Interface
  >>> class IMyInterface(Interface):
  ...   pass
  >>> class SomeClass(object):
  ...   pass
  >>> class MyAdapter(grok.Adapter):
  ...   grok.provides(IMyInterface)
  ...   grok.context(SomeClass)

To grok this adapter, you can simply write this::

  >>> grok.testing.grok_component('MyAdapter', MyAdapter)
  True

We can now use the adapter::

  >>> instance = SomeClass()
  >>> adapter = IMyInterface(instance)
  >>> isinstance(adapter, MyAdapter)
  True

We can use grok_component with only two arguments because we know the
adapter grokker is not looking for more. Sometimes we need to supply
an extra argument however::

  >>> class ISecondInterface(Interface):
  ...   pass
  >>> class SecondAdapter(grok.Adapter):
  ...   grok.provides(ISecondInterface)

This adapter does not supply its own context. Trying to do what we did
before will therefore fail::

  >>> grok.testing.grok_component('SecondAdapter', SecondAdapter)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for <class 'grok.tests.grokker.grokcomponent.SecondAdapter'>, please use the 'context' directive.

So we need to supply the context ourselves::

  >>> grok.testing.grok_component('SecondAdapter', SecondAdapter, context=SomeClass)
  True

Now we can use the SecondAdapter as well::

  >>> adapter = ISecondInterface(instance)
  >>> isinstance(adapter, SecondAdapter)
  True

The next optional argument is module_info and the final argument is
templates.
"""
