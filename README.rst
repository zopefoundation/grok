.. image:: https://github.com/zopefoundation/grok/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/zopefoundation/grok/actions/workflows/tests.yml
    :alt: CI Status
.. image:: https://readthedocs.org/projects/grok/badge/?version=latest
    :target: https://grok.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Grok
****

What is grok?
=============

Grok is a smashing web framework based on `Zope Toolkit`_ technology.

.. _`Zope Toolkit`: https://zopetoolkit.readthedocs.io/en/latest/

Grok uses the Component Architecture and builds on Zope concepts like
content objects (models), views, and adapters.  Its simplicity lies in
using **convention over configuration** and **sensible defaults** when
wiring components together.  That means neither a configuration
language like ZCML nor a lot of repetition are needed to create a web
application with grok.

You can find out much more about Grok at our `website
<https://web.archive.org/web/20221005185405/http://grok.zope.org>`_.

Who is grok?
============

Grok is a friendly caveman from the Stone Age.  He has a big club that
he hunts mammoths with.  He will also use this club to smash anything
he doesn't like.

"ME GROK SMASH ZCML!"

Getting grok
============

The easiest way to get started with grok is to install the
`grokproject <http://cheeseshop.python.org/pypi/grokproject>`_ package
(e.g. via ``easy_install grokproject``) and then create a new project
area by calling the ``grokproject`` script like so::

  $ grokproject MyProject
  ... many lines of output here

This will create a project area in ``MyProject`` as well as download
and install grok.

You can also get grok from GitHub::

  git clone https://github.com/zopefoundation/grok.git

Then follow the instructions in ``INSTALL.rst``.
