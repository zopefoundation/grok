"""
The skin directive is used to trigger the registration of a layer as a
IBrowserSkin type. Since layers are really interface classes, we need
a special directive implementation that will take care of storing data
on the interface.

Import -- and thus "execute" -- the skindirective fixture to make the
directive have effect::

  >>> from grok.tests.skin import directive_fixture

  >>> import grok
  >>> grok.skin.bind().get(directive_fixture.IIsAnInterface)
  'skin_name'

Unfortunately it is not possible to check whether the directive isn't
used on a "normal" class instead of an interface class. This means, the
directive can be *declared* on a normal class, however, using it to
retrieve data will fail due to the way the directive's store is
implemented::

  >>> from grok.tests.skin import directive_onaclass_fixture

  >>> grok.skin.bind().get(directive_onaclass_fixture.NotAnInterfaceClass)
  Traceback (most recent call last):
   ...
  AttributeError: type object 'NotAnInterfaceClass' has no attribute
  'queryTaggedValue'

Note that the directive only supports text (ASCII string or unicode):

  >>> from grok.tests.skin import directive_textonly_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: The 'skin' directive can only be called with unicode or ASCII.

In certain cases we need to set a value on a component as if the directive
was actually used::

  >>> from zope import interface
  >>> class IFoo(interface.Interface):
  ...     pass
  >>> grok.skin.set(IFoo, u'value as set')
  >>> grok.skin.bind().get(IFoo)
  u'value as set'

"""
