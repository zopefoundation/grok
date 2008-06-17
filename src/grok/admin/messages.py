# -*- coding: latin-1 -*-
# Copyright (c) 2007 gocept gmbh & co. kg
# See also LICENSE.txt
# $Id$
"""Support for flash-messages in the grok admin UI."""

import zope.interface
import zope.component

import grok

import z3c.flashmessage.interfaces
import z3c.flashmessage.sources
import z3c.flashmessage.receiver


class Messages(grok.View):

    grok.context(zope.interface.Interface)

    @property
    def messages(self):
        receiver = zope.component.getUtility(
            z3c.flashmessage.interfaces.IMessageReceiver)
        return receiver.receive()



grok.global_utility(z3c.flashmessage.sources.SessionMessageSource,
                    name='session')
grok.global_utility(z3c.flashmessage.receiver.GlobalMessageReceiver)
