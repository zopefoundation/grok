==========
Mars Layer
==========

Martian is a library that allows the embedding of configuration
information in Python code. Martian can then grok the system and
do the appropriate configuration registrations.

This package uses martian to define layers and skins.

The base layers available are:

* mars.layer.IMinimalLayer
  Uses z3c.layer.IMinimalBrowserLayer

* mars.layer.IPageletLayer
  Uses z3c.layer.IPageletBrowserLayer

Example Code
------------

  >>> import mars.layer
  >>> class IMyLayer(mars.layer.IMinimalLayer):
  ...     pass
  >>> class MySkin(mars.layer.Skin):
  ...   mars.layer.layer(IMyLayer)

