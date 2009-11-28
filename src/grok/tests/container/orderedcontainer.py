"""

The grok.OrderedContainer is a a model that is also a container. Unlike plain
grok.Containers, OrderedContainers keep the mapping keys in the order items
were added. It has a dictionary API. It in fact stores its information in a
BTree so you can store a lot of items in a scalable way.

  >>> grok.testing.grok(__name__)

  >>> from zope.container.interfaces import IContainer
  >>> bones = OrderedBones()
  >>> IContainer.providedBy(bones)
  True
  >>> from zope.container.interfaces import IOrderedContainer
  >>> IOrderedContainer.providedBy(bones)
  True
  >>> from zope.container.btree import BTreeContainer
  >>> isinstance(bones, BTreeContainer)
  True

Order is initially determined by the sequence in which items were added (mind
that there is a subscriber to the containermodified event in order to
illustrate an ordered container fires events just like normal containers)::

  >>> bones['thigh'] = Bone('Thigh Bone')
  >>> bones['knee'] = Bone('Knee Cap')
  >>> bones['shin'] = Bone('Shin Bone')
  >>> bones['ankle'] = Bone('Ankle Joint')
  >>> bones.keys()
  ['thigh', 'knee', 'shin', 'ankle']

Now change the order::

  >>> bones.updateOrder(order=['ankle', 'shin', 'knee', 'thigh'])
  >>> bones.keys()
  ['ankle', 'shin', 'knee', 'thigh']

  >>> list(bones.items())
  [('ankle', <grok.tests.container.orderedcontainer.Bone object at ...>),
  ('shin', <grok.tests.container.orderedcontainer.Bone object at ...>),
  ('knee', <grok.tests.container.orderedcontainer.Bone object at ...>),
  ('thigh', <grok.tests.container.orderedcontainer.Bone object at ...>)]

  >>> [bone.name for bone in bones.values()]
  ['Ankle Joint', 'Shin Bone', 'Knee Cap', 'Thigh Bone']

  >>> del bones['knee']
  >>> bones.keys()
  ['ankle', 'shin', 'thigh']

  >>> bones['toe'] = Bone('Toe')
  >>> bones.keys()
  ['ankle', 'shin', 'thigh', 'toe']

Adding a new object under an existing key, raises a DuplicationError::

  >>> bones['shin'] = Bone('Another Shin Bone')
  Traceback (most recent call last):
  ...
  KeyError: u'shin'

Reordering with a wrong set of keys should fail::

  >>> bones.updateOrder(order=['ankle', 'shin', 'knee', 'thigh'])
  Traceback (most recent call last):
  ...
  ValueError: Incompatible key set.

"""

import grok

class OrderedBones(grok.OrderedContainer):
    pass

class Bone(grok.Model):
    def __init__(self, name):
        self.name = name
