===============
Developing Grok
===============

.. contents::

Making Grok releases
--------------------

Manual steps
~~~~~~~~~~~~

Grok's release procedure (and that of the derivatives like the ``grokcore.*``
family of libraries) follows ZTK's `official release guidelines`_.

.. _`official release guidelines`: http://docs.zope.org/zopetoolkit/process/releasing-software.html

Automated steps
~~~~~~~~~~~~~~~

Even if it can be useful to follow these release steps by hand, most of it
is automated in the `zest.releaser`_ package that is included in Grok's
``buildout.cfg``. Using this tool will prevent making mistakes caused by the
rather repetitive nature of the release process.

.. _`zest.releaser`: http://pypi.python.org/pypi/zest.releaser

Part of the `official release guidelines`_ is reviewing the changelog
recorded in ``CHANGES.txt``. This is an important step that cannot be
automated.

In other words, before starting a release make sure that:

  1) All tests pass
  2) All local changes are committed
  3) The changelog is up to date.

The `zest.releaser` package provides a command line utility to help reviewing
the changelog. It will display a diff between the most recently created
release tag and the current maintenance branch of trunk::

  $ ./bin/lasttagdiff

After having reviewed the changelog (and making sure any changes are
commited!) the actual release can be made::

  $ ./bin/fullrelease

Post release steps
~~~~~~~~~~~~~~~~~~

After having released Grok, the following steps should be taken:

1. After having tagged and released Grok, the ``versions.cfg`` for this
   version needs to be uploaded to ``grok.zope.org/releaseinfo``.

   Copy ``versions.cfg`` to ``grok-[VERSION].cfg`` where [VERSION] needs to
   represent the released version. For example ``grok-0.13.cfg``. Add grok's
   version to this file::

     [versions]
     grok = 0.13
     ...

   Then upload this file::

     $ scp ./grok-[VERSION].cfg grok.zope.org:/var/www/html/grok/releaseinfo/

2. Grokproject generates a ``buildout.cfg`` with an ``extends`` directive
   pointing to the most recent release versions file. It determines the URL
   to this versions file by reading http://grok.zope.org/releaseinfo/current.
   This file needs to be updated to point to the uploaded ``*.cfg`` file.

3. Grokproject is able to download and use a tarball containing Grok and
   all packages Grok depends on. This will speed up the initial buildout run.
   To create this tarball use the ``bundlemaker`` command from the Grok
   buildout directory::

     $ ./bin/bundlemaker

4. Then upload the created tarball to ``grok.zope.org/releaseinfo/``::

     $ scp ./grok-eggs-0.13.tgz grok.zope.org:/var/www/html/grok/releaseinfo/

5. Add a document with the release announcement in the `releases folder`_
   Name it after the release version number. Summarize what is in
   ``CHANGES.txt``. Make sure you move it to become the first item of the
   releases folder. You can move it up by using the contents view of the
   folder. The last column in that table presents a handle by which you can
   drag up the document in the folder.

   .. _`releases folder`: http://grok.zope.org/project/releases/

6. Update the `upgrade notes`_ with the latest version as in
   ``doc/upgrade.txt``.

   .. _`upgrade notes`: http://grok.zope.org/project/upgrade-notes

7. Create a news item in the `blog folder`_ announcing the news. The text
   can be based on the release notes written at point 7.

   .. _`blog folder`: http://grok.zope.org/blog/

8. Make both the new release notes, the new news item, as well as the
   updated upgrade notes public.

9. Update the sidebar in the site. You can edit it here:
   http://grok.zope.org/portal_skins/custom/portlet_download/manage_main

10. Community Documentation: Update the Plone Help Center used for Grok
    Community Documentation so that the new Version is available. Important:
    you can select multiple "current" versions for community documentation,
    any documentation for a release which is not "current" gets a big nasty
    "outdated" header at the top of it. We only want to do this for
    documentation which is truly outdated and no longer best practice. Do
    this here: http://grok.zope.org/documentation/edit

11. Official Documentation: Create a build of the docs from the tagged
    release and copy it to the server. Detailed steps are documented in the
    `Updating the Official Grok Documentation (OGD)`_ page.

12. Send out an email to at least zope-announce@zope.org as well as grok-
    dev@zope.org announcing the new release. The text can be based on the
    release notes written at point 7.

13. Update the Grok Wikipedia article with the information about the
    latest release: http://en.wikipedia.org/wiki/Grok_(web_framework)

.. _`Updating the Official Grok Documentation (OGD)`: http://grok.zope.org/project/meta/updating-the-official-grok-documentation-ogd

Binary eggs on Windows
----------------------

Grok aims to work on Windows as well. This is not a problem for the
most part, but takes special attention when updating the list of
dependencies.  The follow eggs need a compiler on Unixy platforms, and
a binary egg on Windows::

  zope.i18nmessageid
  zope.interface
  zope.security
  zope.container
  ZODB3
  zope.hookable
  zope.proxy

Please make sure a Windows version of the egg is available when you
update a dependency!

