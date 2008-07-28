"""
The skin directive is used to trigger the registration of a layer as a
IBrowserSkin type. Since layers are really interface classes, we need a special
directive implementation that will take care of storing data on the interface.

Import - and thus "execute" the skindirective fixture to make the directive
have effect::

   >>> from grok.tests.directive import skindirective_fixture

   >>> import grok
   >>> print grok.skin.bind().get(skindirective_fixture.IIsAnInterface)
   skin_name

Unfortunately it is not possible to check whether the directive isn't used on a
"normal" class instead of an interface class. This means, the directive can be
*declared* on a normal class, however, using it to retrieve data will fail due
to the way the directive's store is implemented::

   >>> from grok.tests.directive import skindirectiveonaclass_fixture

   >>> print grok.skin.bind().get(
   ...     skindirectiveonaclass_fixture.NotAnInterfaceClass)
   Traceback (most recent call last):
   ...
   AttributeError: type object 'NotAnInterfaceClass' has no attribute
   'queryTaggedValue'
"""
