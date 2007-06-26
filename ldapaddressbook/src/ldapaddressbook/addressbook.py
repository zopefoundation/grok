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



class AddressBook(grok.Application):

    def traverse(self, name):
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
        cn = schema.TextLine(title=u"LDAP CN", readonly=True)

        givenName = schema.TextLine(title=u"First name", required=False)
        sn = schema.TextLine(title=u"Last name")
        initials = schema.TextLine(title=u"Initials", required=False)

        # jpegPhoto
        description = schema.TextLine(title=u"Description", required=False)

        title = schema.TextLine(title=u"Title", required=False)

        o = schema.TextLine(title=u"Organisation", required=False)
        ou = schema.TextLine(title=u"Organisational Unit", required=False)
        businessRole = schema.TextLine(title=u"Role", required=False)

        category = schema.TextLine(title=u"Category", required=False)

        mail = schema.List(title=u"Email", required=False,
                value_type=schema.TextLine())

        telephoneNumber = schema.TextLine(title=u"Phone (business)", required=False)
        mobile = schema.TextLine(title=u"Mobiltelefon", required=False)
        facsimileTelephoneNumber = schema.TextLine(title=u"Telefax (business)", required=False)
        homePhone = schema.TextLine(title=u"Phone (private)", required=False)

        note = schema.TextLine(title=u"Note", required=False)

        postalAddress = schema.Text(title=u"Address (business)", required=False)
        postalCode = schema.TextLine(title=u"ZIP", required=False)
        street = schema.TextLine(title=u"Street", required=False)
        l = schema.TextLine(title=u"City", required=False)
        st = schema.TextLine(title=u"State", required=False)

        homePostalAddress = schema.Text(title=u"Address (private)", required=False)

        labeledURI = schema.TextLine(title=u"Homepage", required=False)

    def __init__(self, cn):
        # Initialize from LDAP data
        data = get_contact(cn)
        if data is not None:
            for field in grok.schema_fields(Contact):
                field_data = data.get(field.__name__)
                if not field_data:
                    continue
                if isinstance(field, schema.TextLine):
                    setattr(self, field.__name__, field_data[0])
                elif isinstance(field, schema.Text):
                    setattr(self, field.__name__, '\n'.join(field_data))
                elif isinstance(field, schema.List):
                    setattr(self, field.__name__, field_data)
                else:
                    raise TypeError, "Invalid schema field type: %r" % field

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        store_contact(self)


class EditContact(grok.EditForm):
    grok.context(Contact)
    grok.name("index")

    @grok.action("Apply")
    def apply(self, action, data):
        # XXX UI feedback and modification event triggering
        self.context.update(data)


# LDAP helper functions

def get_contact_list():
    l = ldap.initialize(LDAP_SERVER)
    l.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
    results = l.search_s(LDAP_SEARCH_BASE, ldap.SCOPE_SUBTREE, "(objectclass=inetOrgPerson)")
    import pprint
    pprint.pprint(results)
    if results is None:
        return []
    cns = [unicode(x[1]['cn'][0], 'utf-8') for x in results]
    cns.sort()
    return cns

def get_contact(cn):
    l = ldap.initialize(LDAP_SERVER)
    l.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
    results = l.search_s(LDAP_SEARCH_BASE,
                         ldap.SCOPE_SUBTREE,
                         "(&(objectclass=inetOrgPerson)(cn=%s))" % cn)
    if results:
        # Get data dictionary
        data = results[0][1] 
        for key, value in data.items():
            value = [unicode(v, 'utf-8') for v in value]
            data[key] = value
        return data

def store_contact(contact):
    l = ldap.initialize(LDAP_SERVER)
    l.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)
    dn = "cn=%s,%s" % (contact.cn.encode('utf-8'), LDAP_SEARCH_BASE)

    modlist = []
    for field in  grok.schema_fields(contact):
        value = field.get(contact)
        if value is None:
            value  = []
        elif isinstance(field, schema.Text):
            value = value.split("\n")
        elif not isinstance(value, list):
            value = [value]
        value = map(lambda x:x.encode('utf-8'), value)

        modlist.append((ldap.MOD_REPLACE, field.__name__, value))
    l.modify_s(dn, modlist)
