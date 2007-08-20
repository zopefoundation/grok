=====================
A basic grok admin UI
=====================

The internal name of the admin UI is:
Grok Application Interface Application or, for short GAIA.

GAIA is itself a Grok application and a subproject to the core Grok
development. Its main goal is making developing of Zope 3 and Grok
applications a faster and smarter job with more fun for everybody.


Login - what is my username/password?
-------------------------------------

Before you can use the admin UI, you first must log in.

The username and password of the manager principal (kind of super
user) can be found in the file ``buildout.cfg`` in the root of your
subversion checkout. 

In case you do not know, what 'subversion checkout' means, look for a
file ``site.zcml`` in your installation.

Users of ``grokproject``, might find this file in
``<installdir>/parts/app/site.zcml``.


Using the admin-UI
------------------

After login you can visit some of the main management topics, as
described below:

On top of the admin-UI you can always find three links to the main
management activities currently possible with GAIA:


Applications
------------

* List of all instanciated applications

* You can add new instances of Grok applications

* For each installed application you can directly call:

  - the object browser (telling you more about this concrete object)

  - the class browser (telling you more about the class of your app)

* For each available application type you can directly call:

  - the class browser (telling you more about the class of your app)

* You can delete your installed applications.


Server
------

* Start/Restart the server. Caution! This does not work, if the server
  was started in 'foreground mode' (with 'zopectl fg').

* Get basic information about the running Zope system.

* Enter a message to be displayed on top. You can, for example, leave
  a message here for your co-admins. To delete the message, just enter
  the empty string in the appropriate input box.


Documentation
-------------

* From here you get starting points to the more elaborated
  documentation features of Grok, namely:

  - The object browser:

    helps browsing the ZODB and other objects.

  - The class browser:

    gives documentation to classes, packages and other things, which
    are not instances.


Bugs, Caveats and Ways to Get Help
----------------------------------

The Grok admin UI was developed basically during a Google Summer of
Code project.

It is still full of bugs.

For bugreports use:

    https://launchpad.net/grok

For discussions subscribe to the ``grok-dev`` mailing list, hosted on:

    http://lists.zope.org.

The projects' home is the grok subversion repository at:

    http://svn.zope.org/grok/

Grok's cave can be found at

    http://grok.zope.org/

Enjoy!
