"""

We define a grokker AlphaGrokker for a component called Alpha. We first need to
grok the module defining the grokkers, in order to get them registered.

Usually this would be triggered from a meta.zcml in a package, that would grok
the module containing the grokkers (e.g. meta.py).

We do it manually now::

  >>> import grok
  >>> grok.testing.grok('grok.tests.grokker.onlyonce_fixture._meta')

This _meta.py module then will be grokked again during 'normal' grok time. Grok
will not re-register the grokkers as this could have unwanted side-effects. It
will grok the components of course.

NOTE: the module is called _meta to make sure it is grokked (although its
grokker registration should be ignored) before the other files. The modules are
picked up in alphabetical order.

To simulate this, we grok the whole package::

  >>> grok.testing.grok('grok.tests.grokker.onlyonce_fixture')
  alpha

"""
