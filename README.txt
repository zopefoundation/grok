Grok
****

What is grok?
=============

Grok makes it easier to get started with a Zope 3 web application.

Grok uses the Component Architecture and builds on Zope 3 concepts
like content objects (models), views, and adapters.  Its simplicity
lies in using **convention over configuration** and **sensible
defaults** when wiring components together.  That means neither a
configuration language like ZCML nor a lot of repetition are needed to
create a web application with grok.

You can find out much more about Grok at our http://grok.zope.org
website.

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
and install grok and Zope 3 (the application server grok is built on).

You can also get grok from the subversion repository::

  svn co svn://svn.zope.org/repos/main/grok/trunk grok

Then follow the instructions of ``INSTALL.txt``.
