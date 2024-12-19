=============
The grok wiki
=============

The grok wiki is our first demo application, used to demonstrate how grok can
be used to efficiently write web applications with Zope 3.

It is not so much intended as a tutorial, but as a test bed for ourselves and
to provide guidance for new users how we are using grok ourselves.

Installation
============

In the ``grok`` directory (the one above ``grokwiki``)  run:

* python3 -m venv .
* bin/pip install zc.buildout
* bin/buildout -c grokwiki.cfg
* bin/paster serve parts/etc/deploy.ini
* Access via http://localhost:8080/ with username and password ``grok``.
* Create a new wiki page.
