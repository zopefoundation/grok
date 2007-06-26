=================
LDAP address book
=================

A grok example application that shows how to load and store objects from
external data sources.


Dependencies
------------

  - Requires python-ldap (no egg available yet)


Issues
------

  - grok.EditForm gives no chance to perform a single update with the data of
    all forms

  - Container (AddressBook) has to set __parent__ and __name__ for the
    dynamically created contacts 

  - Mapping outside schemata to inside schema is tedious

  - formlib acquires standard ZMI layout
