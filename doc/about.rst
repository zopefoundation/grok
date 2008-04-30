======================================
Grok: now even cavemen can use Zope 3
======================================

Grok is a web application framework for Python developers. It is aimed
at both beginners and very experienced web developers. Grok has an
emphasis on agile development. Grok is easy *and* powerful.

Grok: Experience, Expertise, Extensibility
------------------------------------------

You will likely have heard about many different web frameworks for
Python as well as other languages. Why you should you consider Grok?

* Grok offers a *lot* of building blocks for your web application.

* Grok is informed by a *lot* of hard-earned wisdom.

Grok accomplishes this by being based on Zope 3, an advanced
object-oriented web framework. While Grok is based on Zope 3, and
benefits a lot from it, you do not need to know Zope at all in order
to get productive with Grok.

Grok is agile
.............

Grok doesn't require you to edit cryptic configuration files. Instead
you just program in Python and create HTML templates. Beyond this,
Grok also offers a wide range of built-in features at your fingertips,
from automated form generation to an object database. This way, Grok
gives you both power and quick satisfaction during development. Grok
is *fun*.

Grok has an extensive tutorial_ that helps you to get started. And
thanks to grokproject_, you'll be able to create your first web app
with Grok in no time.

.. _tutorial: tutorial.html

.. _grokproject: http://cheeseshop.python.org/pypi/grokproject

Grok offers a very wide range of features
.........................................

Through Zope 3, Grok offers a very wide range of building blocks for
your web application. What's more, Zope 3 components are typically
rock-solid due to extensive unit-testing and well-specified API
documentation.

Grok is grounded in a deep experience with web development
..........................................................

Grok, through Zope 3, is informed by hard-earned wisdom. Zope 3 is a
powerful and flexible web application framework for Python that has
been under continuous development since 2001.  Zope 3's design in turn
is based on experience with the Zope 2 platform, which has been under
continuous development (starting with Bobo, Principia and then Zope 1)
since 1997. The Zope community is supported by an independent
foundation, the Zope Foundation. 

The Zope community has been around for a while. We've built a lot and
learned a lot. We are in this for the long run.

Grok for the future
...................

Successful web applications aren't built for a day - such an
application will need to be maintained, extended, evolved, over a
period of many years. Zope developers really know this. Grok, through
Zope 3, offers an architecture that enables your application to grow
over time.


Grok: Zope 3 for cavemen
------------------------

Grok stands on a giant's shoulder. That giant is Zope 3.

Zope 3 is an advanced object oriented web framework. Zope 3 features a
large amount of API documentation and aims for reliability. It has a
very large automatic test coverage (many thousands of tests). It has a
large set of core features, and sports an enormous range of plug-in
components.

The Grok developers think Zope 3 is great. Zope 3, unfortunately, also
has some problems: its power raises the entry barrier for developers
to get up to speed with it. Even after you've learned it, Zope 3's
emphasis on explicit configuration and specification of interfaces can
slow down development.

Grok aims to remedy these problems. Grok aims to make Zope 3 easier to
learn, and more agile to work with, while retaining the power of Zope
3.

Grok appeals to the caveman or woman in all of us. Cavemen, like us
programmers, want powerful and flexible tools. Cavemen are great at
tools after all; they invented the whole concept of them. But cavemen,
and we, also want our tools to be simple and effective.

Cavemen want tools like clubs: a club is powerful, flexible (you can
bash in anything, mash potatoes too) and also simple and
effective. Zope 3 is already powerful and flexible. Grok aims to make
it simpler and more effective, for beginners and experienced
developers alike. Grok: now even cavemen can use Zope 3.

Grok from the Zope 3 perspective
--------------------------------

Zope 3 allows you to combine different components in an explicit,
flexible way. You can hook up a view to a model, an event handler to
an event, and a new API to an existing object. The process of doing
this is called *configuration*. In a technical sense, Grok can be
understood as an alternate configuration mechanism for Zope 3.

Zope 3 without Grok uses ZCML for hooking up objects together. ZCML is
an XML-based configuration language. ZCML statements are stored in
their own file, next to the code. While using ZCML has the benefit of
being explicit and flexible, it can also make code harder to read as
there are more files to consult in order to understand what is going
on.

Grok does away with ZCML. Instead it analyzes your Python code for the
use of certain special base classes and directives, and then "groks"
it. This grokking process results in the same configuration as it
would have if you used the equivalent ZCML. We believe that having all
configuration along with your Python code makes the code easier to
follow and more fun to develop.

Grok has been designed so that if you organize your code in a certain
way, you can even leave out most of the explicit directives in your
Python code. This makes code written for Grok look clean and
uniform. You still have all the power of explicit configuration
available should you need it, however.

During the development of Grok we have taken a careful look at common
patterns in Zope 3 code and configuration. Grok aims to make these
patterns easier to use and more succinct.
