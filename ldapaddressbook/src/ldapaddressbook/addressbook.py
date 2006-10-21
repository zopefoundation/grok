##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""The grok LDAP address book.
"""

import ldap

from zope import schema

import grok


LDAP_SERVER = "ldap://ldaphost:389"
LDAP_LOGIN = "cn=admin,dc=example,dc=com"
LDAP_PASSWORD = "password"
LDAP_SEARCH_BASE = "ou=Addresses,dc=example,dc=com"


class AddressBook(grok.Model):

    @grok.traverse
    def getContact(self, name):
        contact = Contact(name)
        contact.__parent__ = self
        contact.__name__ = name
        return contact

    def listContacts(self):
        return get_contact_list()


class AddressBookListing(grok.View):
    grok.context(AddressBook)
    grok.name("index")


addressbooklisting = grok.PageTemplate("""\
<html>
<body>
<ul>
    <li tal:repeat="contact context/listContacts">
        <a tal:attributes="href string:${context/@@absolute_url}/$contact" tal:content="contact">Peter Kummer</a></li>
</ul>
</body>
</html>""")


class Contact(grok.Model):

    class fields:
        cn = schema.TextLine(title=u"Display name")
        #displayName = fileAs

        givenName = schema.TextLine(title=u"First name")
        sn = schema.TextLine(title=u"Last name")
        initials = schema.TextLine(title=u"Initials")

        # jpegPhoto
        description = schema.TextLine(title=u"Description")

        title = schema.TextLine(title=u"Title")

        o = schema.TextLine(title=u"Organisation")
        ou = schema.TextLine(title=u"Organisational Unit")
        businessRole = schema.TextLine(title=u"Role")

        category = schema.TextLine(title=u"Category")

        mail = schema.TextLine(title=u"Email")

        telephoneNumber = schema.TextLine(title=u"Phone (business)")
        mobile = schema.TextLine(title=u"Mobiltelefon")
        facsimileTelephoneNumber = schema.TextLine(title=u"Telefax (business)")
        homePhone = schema.TextLine(title=u"Phone (private)")
        otherPhone = schema.TextLine(title=u"Phone (other)")

        note = schema.TextLine(title=u"Note")

        postalAddress = schema.Text(title=u"Address (business)")
        postalCode = schema.TextLine(title=u"ZIP")
        street = schema.TextLine(title=u"Street")
        l = schema.TextLine(title=u"City")
        st = schema.TextLine(title=u"State")

        homePostalAddress = schema.Text(title=u"Address (private)")
        otherPostalAddress = schema.Text(title=u"Address (other)")

        labeledURI = schema.TextLine(title=u"Homepage")

    def __init__(self, cname):
        # Initialize from LDAP data
        data = get_contact(cname)
        if data is not None:
            for field in grok.schema_fields(Contact):
                field_data = data.get(field.__name__)
                if not field_data:
                    continue
                if isinstance(field, schema.TextLine):
                    setattr(self, field.__name__, field_data[0])
                elif isinstance(field, schema.Text):
                    setattr(self, field.__name__, '\n'.join(field_data))
                else:
                    raise TypeError, "Invalid schema field type: %r" % field


class EditContact(grok.EditForm):
    grok.context(Contact)
    grok.name("index")


# LDAP helper functions

def get_contact_list():
    l = ldap.initialize(LDAP_SERVER)
    l.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
    results = l.search_s(LDAP_SEARCH_BASE, ldap.SCOPE_SUBTREE, "(objectclass=inetOrgPerson)")
    if results is None:
        return []
    cnames = [unicode(x[1]['cn'][0], 'utf-8') for x in results]
    cnames.sort()
    return cnames

def get_contact(cname):
    l = ldap.initialize(LDAP_SERVER)
    l.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
    results = l.search_s(LDAP_SEARCH_BASE,
                         ldap.SCOPE_SUBTREE,
                         "(&(objectclass=inetOrgPerson)(cn=%s))" % cname)
    if results:
        # Get data dictionary
        data = results[0][1] 
        for key, value in data.items():
            value = [unicode(v, 'utf-8') for v in value]
            data[key] = value
        return data
