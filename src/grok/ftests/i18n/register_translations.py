##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
"""
==============================
grok.localesdir
==============================

With Grok a set of translations can be provided by using
grok.i18n.registerTranslation(). The directive takes an [optional]
directory path as only argument, which is computed relative to the
defining module.

The directive is a module-level single text directive, which can be
used several times.

If no translatios directory is given, `locales` will serve as
default value.

The default locales dir, is also searched for translations, if no
explicit call to ``localesdir`` was done. This means, that
if you do not specify a locales directory in a module and a locales
directory with translations exist, this directory will be registered
and the translations therein are provided.

  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We fetch the ZMI translation overview, to check whether the mammoth
domain is registered as translation domain::

  >>> browser.open("http://localhost/++etc++process/@@TranslationDomain.html")
  >>> contents = browser.contents
  >>> '<a href="?RELOAD=&amp;domain=mammoth&amp;language=en">' in contents
  True

Now let's see, whether i18n really works. First we create an
I18nSavannah, which will automatically contain an I18nMammoth called
'manfred'::

  >>> browser.open("http://localhost")
  >>> subform = browser.getForm(name='I18nSavannah')
  >>> subform.getControl('Name your new app:').value = 'mysavannah'
  >>> subform.getControl('Create').click()

  >>> print browser.contents
  <html xmlns="http://www.w3.org/1999/xhtml">
  ...
  ...<legend>Installed applications</legend>
  ...
  ...<a href="http://localhost/mysavannah">
  ...

We watch manfred::

  >>> browser.open("http://localhost/mysavannah/manfred")
  >>> print browser.contents
  <html>
  ...<div>A mammoth</div>
  ...This mammo is called Manfred
  ...

This is the english translation. See, what we get, if we require
German docs::

  >>> browser.addHeader('Accept-Language', 'de_DE')
  >>> browser.open("http://localhost/mysavannah/manfred")
  >>> print browser.contents
  <html>
  ...<div>Mammut</div>
  ...Dieses Mammut wird Manfred genannt.
  ...

"""
import grok
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('mammoth')

# Here we register the local translations dir using the default value
# ('locales'). This is not neccessary, because the 'locales' dir would
# be searched by default for translations. But calling it explicitly,
# we provoke complains about missing directories.
grok.localesdir('locales')

class I18nSavannah(grok.Application, grok.Container):
    """A place for mammoths.
    """
    def __init__(self, *args, **kw):
        super(I18nSavannah, self).__init__(*args, **kw)
        self['manfred'] = I18nMammoth()

class I18nMammoth(grok.Model):
    """An internationalized mammoth.
    """
    name = _(u'Manfred')

    def getName(self):
        return _(u'mammoth-is-called',
                 u"This mammoth is called: ${name}",
                 mapping={'name':self.name}
                 )

class I18nMammothView(grok.View):
    """An internationalized view.
    """
    grok.context(I18nMammoth)
    grok.name('index')
