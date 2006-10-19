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

We had problems when switching to grok.Container with the __parent__ attribute
being set, we better make sure this doesn't happen again:

    >>> skull = Bone()
    >>> print skull.__parent__
    None
    >>> print skull.__name__
    None
    >>> bag['skull'] = skull
    >>> skull.__parent__
    <grok.tests.container.container.BoneBag object at 0x...>
    >>> skull.__name__
    u'skull'

"""

import grok

class BoneBag(grok.Model, grok.Container):
    pass

class Bone(grok.Model):
    pass
