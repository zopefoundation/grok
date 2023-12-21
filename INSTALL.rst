Developing grok
===============

Preparing for grok development
------------------------------

The Grok development sandbox is set up via `zc.buildout`_

.. _zc.buildout: https://pypi.org/project/zc.buildout

Clone ``grok`` from Github:

    $ git clone git@github.com:zopefoundation/grok.git

Go inside this directory and create a ``venv`` and install ``zc.buildout``:

    $ cd grok
    $ python3 -m venv .
    $ bin/pip install zc.buildout

and run the buildout command::

    $ bin/buildout
    [lots of stuff will be downloaded and installed here, ignore the warnings]

Note that if you have more than one sandbox for a Zope-based web
application, it will probably make sense to share the eggs between the
different sandboxes.  You can tell zc.buildout to use a central eggs
directory by creating ``~/.buildout/default.cfg`` with the following
contents::

    [buildout]
    eggs-directory = /home/bruno/buildout-eggs

Note, that this is the grok core package. If you want to develop Grok
applications you might consider to use `grokproject
<http://pypi.python.org/pypi/grokproject>`_ instead.


Running the demo application
----------------------------

You can start Zope with the demo application installed with the
following command:

    $ bin/paster serve parts/etc/deploy.ini

If you now connect to port 8080 and log in with username 'grok',
password 'grok', you should be able to add the grok-based applications
(such as grokwiki) from the menu.

Running the tests
-----------------

Grok's tests are easily run by executing the test runner that's
installed in the ``bin`` directory::

    $ bin/test

Generating the documentation
----------------------------

Grok's tutorial documents can easily be generated using the following call::

    $ tox -e docs
