"""
After grokking a module that defines an application, the application factory is
available as a utility::

    >>> grok.testing.grok(__name__)
    >>> import zope.component
    >>> import grokcore.site.interfaces
    >>> calendar_app = zope.component.getUtility(
    ...     grokcore.site.interfaces.IApplication,
    ...     name='grok.tests.application.application.Calendar')
    >>> calendar_app
    <class 'grok.tests.application.application.Calendar'>

Applications are both containers and sites::

    >>> issubclass(calendar_app, grok.Site)
    True

Applications can be instanciated without any arguments::

    >>> calendar = calendar_app()
    >>> calendar
    <grok.tests.application.application.Calendar object at 0x...>

"""

import grok

class Calendar(grok.Application):
    """A calendar application that knows about ancient
    calendar systems from the stone age.
    """
