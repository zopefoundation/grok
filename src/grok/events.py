##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Events for Grok application components.

The events described here are *not* trigged by Grok itself. They are
conveniently provided to be used in your own application.

"""
from zope.interface import implementer
from zope.interface.interfaces import ObjectEvent
from grok.interfaces import IDatabaseCreatedEvent


@implementer(IDatabaseCreatedEvent)
class DatabaseCreatedEvent(ObjectEvent):
    pass
