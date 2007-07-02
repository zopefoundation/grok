============
Megrok Layer
============

This package is part of an attempt to use the wonderful tools provided in the
z3c namespace to the grok cave.

The grok.ILayer provides IDefaultBrowser, megrok.layer provides IMinimalLayer
and IPageletLayer which respectively provide z3c.minimal.IMinimalBrowserLayer
and z3c.layer.pagelet.IPageletBrowserLayer. Both of which provide
IBrowserRequest but *not* IDefaultLayer.

More about these layers can be found in z3c.layer.*.README's.
