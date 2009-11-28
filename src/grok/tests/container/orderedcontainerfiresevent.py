"""
Mind that there is a subscriber to the containermodified event in order to
illustrate an ordered container fires events just like normal containers::

  >>> grok.testing.grok(__name__)
  >>> bones = OrderedBones()

Add an item::

  >>> bones['thigh'] = Bone('Thigh Bone')
  Container has changed!

Now change the order::

  >>> bones.updateOrder(order=['thigh'])
  Container has changed!

Delete an item::

  >>> del bones['thigh']
  Container has changed!
  >>> bones.keys()
  []

"""

import grok

class OrderedBones(grok.OrderedContainer):
    pass

class Bone(grok.Model):
    def __init__(self, name):
        self.name = name

from zope.container.interfaces import IContainerModifiedEvent
@grok.subscribe(OrderedBones, IContainerModifiedEvent)
def container_changed(object, event):
    print 'Container has changed!'
