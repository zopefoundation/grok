"""
A viewlet is not allowed to define its own render method and have a template
associated with it at the same time.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  zope.configuration.config.ConfigurationExecutionError: martian.error.GrokError: Multiple possible ways to render viewlet <class 'grok.tests.viewlet.viewlet_render_and_template.Viewlet'>. It has both a 'render' method as well as an associated template.
"""  # noqa: E501

from zope.interface import Interface

import grok


class ViewletManager(grok.ViewletManager):
    grok.name('foo')
    grok.context(Interface)


class Viewlet(grok.Viewlet):
    grok.viewletmanager(ViewletManager)
    grok.context(Interface)

    def render(self):
        return "Render method but also a template!"
