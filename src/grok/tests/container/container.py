"""

The grok.Container is a a model that is also a container.  It has a
dictionary API. It in fact stores its information in a BTree so
you can store a lot of items in a scalable way.

    >>> grok.testing.grok(__name__)

    >>> from zope.container.interfaces import IContainer
    >>> bag = BoneBag()
    >>> IContainer.providedBy(bag)
    True

    >>> from zope.container.btree import BTreeContainer
    >>> isinstance(bag, BTreeContainer)
    True

We had problems when switching to grok.Container with the __parent__ attribute
being set, we better make sure this doesn't happen again:

    >>> skull = Bone()
    >>> skull.__parent__ is None
    True
    >>> skull.__name__ is None
    True
    >>> bag[b'skull'] = skull
    >>> skull.__parent__
    <grok.tests.container.container.BoneBag object at 0x...>
    >>> print(skull.__name__)
    skull

"""

import grok


class BoneBag(grok.Container):
    pass


class Bone(grok.Model):
    pass
