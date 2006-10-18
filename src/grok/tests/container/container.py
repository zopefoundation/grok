"""

The grok.Container is just a convenient subclass of the BTreeContainer that lives in the Zope 3 core:

    >>> grok.grok(__name__)

    >>> from zope.app.container.interfaces import IContainer
    >>> bag = BoneBag()
    >>> IContainer.providedBy(bag)
    True

    >>> from zope.app.container.btree import BTreeContainer
    >>> isinstance(bag, BTreeContainer)
    True

"""

import grok

class BoneBag(grok.Model, grok.Container):
    pass
