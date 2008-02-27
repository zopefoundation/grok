========================================
Navigating To Transient Objects Tutorial
========================================

:Author: Brandon Craig Rhodes

Introduction
------------

If you have already read the Grok tutorial,
you are familiar with the fact that behind Grok
lives a wonderful object database called the *Zope Object Database*,
or the *ZODB* for short.
Thanks to the magic of this database,
your web apps can create Python objects
that are automatically saved to disk
and are available every time your application runs.
In particular,
every ``grok.Model`` and ``grok.Container`` object you generate
can be written safely to your application's ``Data.fs`` file.

But sometimes you need to create objects
that do not persist in the ZODB,
wonderful though it is.
Sometimes these will be objects you design yourself
but have no need to save once you are done displaying them,
like summary statistics or search results.
On other occasions,
you will find yourself using libraries or packages written by other people
and will need to present the objects they return in your Grok app —
whether those objects are LDAP entries,
file system directory listings,
or rows from a relational database.

For the purpose of this tutorial,
we are going to call all such objects *transient* objects.
This highlights the fact that,
from the point of view of Grok,
they are going to be instantiated on-the-fly as a user visits them.
Of course,
they might (or might not) persist in some other application,
like a file system or LDAP server or relational database!
But as far as Grok can tell,
they are being created the moment before they are used
and then, very often, pass right back out of existence —
and out of your application's memory —
once Grok is finished composing the response.

To try out the examples in this tutorial,
start a Grok project named ``TransientApp``
and edit the ``app.py`` and other files
that you are instructed to create or edit.

Choosing a method
-----------------

In this tutorial,
we introduce four methods for creating an object
which you need to present on the web:

* Creating it in your View's ``update()``, using no external data.
* Creating it in your View's ``update()``, using URL or form data.
* Creating it in a ``Traverser`` that gets called for certain URLs.
* Creating it in a ``Container`` that gets called for certain URLs.

To choose among these methods,
the big question you need to ask yourself
is whether the object you are planning to display
is one that will live at its own particular URL or not.
There are three basic relationships we can imagine
between an object on a web page and the URL of the page itself.

The simplest case,
which is supported by the *first* method listed above,
is when you need to create an object
during the rendering of a page that already exists in your application.
An example would be decorating the bottom of your front page
with a random quotation
selected by instantiating a ``RandomQuotation`` class you have written,
so that each time a user reloads the page they see a different quote.
None of the quotations would thereby have URLs of their own;
there would, in fact, be no way for the user
to demand that a particular quotation be displayed;
and the user could not force the site to display again
a quote from Bertrand Russell
that they remember enjoying yesterday but have forgotten.
Such objects can simply be instantiated
in the ``update()`` method of your View,
and this technique will be our first example below.

The situation is only slightly more complex
when you need to use form parameters the user has submitted
to tailor the object you are creating.
This is very common when supporting searching of a database:
the user enters some search terms,
and the application needs to instantiate an object —
maybe a ``SearchResult`` or a ``DatabaseQuery`` —
using those user-provided search terms,
so that the page template can loop across and display the results.
The *second* method listed above is best for this;
since the form parameters are available in the ``update()`` method,
you are free to use them when creating the result object.
This will be the technique illustrated in our second example below.

Finally,
the really interesting case is when an object actually gets its own URL.
You are probably already familiar with several kinds of object
which have their own URLs on the Web —
such as books on Amazon.com, photographs on Flickr, and people on Facebook,
all of which live at their own URL.
Each web site has a particular scheme
which associates a URL with the object it names or identifies.
You can probably guess, for example, just by looking at them,
which object is named by each of the following three Amazon URLs::

 http://www.amazon.com/Web-Component-Development-Zope-3/dp/3540223592
 http://www.amazon.com/Harry-Potter-Deathly-Hallows-Book/dp/0545010225
 http://www.amazon.com/J-R-R-Tolkien-Boxed-Hobbit-Rings/dp/0345340426

The Grok framework, of course,
already supports URL traversal for persistent objects in the ZODB;
if you create a ``Container`` named ``polygons``
that contains two objects named ``triangle`` and ``square``,
then your Grok site will already support URLs like::

 http://yoursite.com/app/polygons/triangle
 http://yoursite.com/app/polygons/square

But the point of this tutorial, of course,
is how you can support URL traversal
for objects which are *not* persistent,
which you will create on-the-fly once someone looks up their URL.
And the answer is that, to support such objects,
you will choose between the last two methods listed above:
you will either create a custom ``Traverser``,
or actually define your own kind of ``Container``,
that knows how to find and instantiate the object the URL is naming.
These two techniques are described last in this tutorial,
because they involve the most code.

But before starting our first example,
we need to define an object that we want to display.
We want to avoid choosing an obvious example,
like an object whose data is loaded from a database,
because then this tutorial would have to teach database programming too!
Plus, you would have to set up a database just to try the examples.
Instead,
we need an object
rich enough to support interesting attributes and navigation,
but simple enough
that we will not have to reach outside of Python to instantiate it.

Our Topic: The Natural Numbers
------------------------------

To make this tutorial simple,
we will build a small web site
that lets the user visit what some people call the *natural numbers*:
the integers beginning with *1*
and continuing with *2*, *3*, *4*, and so forth.
We will define a ``Natural`` class
which knows a few simple things about each number —
like which number comes before it, which comes after it,
and what its prime factors are.

We should start by writing a test suite for our ``Natural`` class.
Not only is writing tests before code an excellent programming practice
that forces you to think through how your new class should behave,
but it will make this tutorial easier to understand.
When you are further down in the tutorial,
and want to remember something about the ``Natural`` class,
you may find yourself re-reading the tests instead of the code
as the fastest way to remember how the class behaves!

The reason this test will be so informative
is that it is a Python “doctest”,
which intersperses normal text with the example Python code.
Create a file in your Grok instance named ``src/transient/natural.txt``
and give it the following contents::

 
               A Simple Implementation of Natural Numbers
 
 The "natural" module of this application provides a simple class for
 representing any postive integer, named "Natural".
 
     >>> from transient.natural import Natural
 
 To instantiate it, provide a Python integer to its constructor:
 
     >>> three = Natural(3)
     >>> print 'This object is known to Python as a "%r".' % three
     This object is known to Python as a "Natural(3)".
     >>> print 'The number of the counting shall be %s.' % three
     The number of the counting shall be 3.
 
 You will find that there are very many natural numbers available; to
 help you navigate among them all, each of them offers a "previous" and
 "next" attribute to help you find the ones adjacent to it.
 
     >>> print 'Previous: %r  Next: %r' % (three.previous, three.next)
     Previous: Natural(2)  Next: Natural(4)
 
 Since we define the set of "natural numbers" as beginning with 1, you
 will find that the number 1 lacks a "previous" attribute:
 
     >>> hasattr(three, 'previous')
     True
     >>> one = Natural(1)
     >>> hasattr(one, 'previous')
     False
     >>> one.previous
     Traceback (most recent call last):
      ...
     AttributeError: There is no natural number less than 1.
 
 You can also ask a number to tell you which prime factors must be
 multiplied together to produce it.  The number 1 will return no
 factors:
 
     >>> one.factors
     []
 
 Prime numbers will return only themselves as factors:
 
     >>> print Natural(2).factors, Natural(11).factors, Natural(251).factors
     [Natural(2)] [Natural(11)] [Natural(251)]
 
 Compound numbers return several factors, sorted in increasing order,
 and each appearing the correct number of times:
 
     >>> print Natural(4).factors
     [Natural(2), Natural(2)]
     >>> print Natural(12).factors
     [Natural(2), Natural(2), Natural(3)]
     >>> print Natural(2310).factors
     [Natural(2), Natural(3), Natural(5), Natural(7), Natural(11)]
 
 Each natural number can also simply return a boolean value indicating
 whether it is prime, and whether it is composite.

     >>> print Natural(6).is_prime, Natural(6).is_composite
     False True
     >>> print Natural(7).is_prime, Natural(7).is_composite
     True False


Next,
we need to tell Grok about this doctest.
Create a file in your instance named ``src/transient/tests.py``
that looks like:

.. code-block:: python

 import unittest
 from doctest import DocFileSuite

 def test_suite():
     return unittest.TestSuite([ DocFileSuite('natural.txt') ])


You should now find that running ``./bin/test`` inside of your instance
now results in a whole series of test failures.
This is wonderful and means that everything is working!
At this point Grok is able to find your doctest,
successfully execute it,
and correctly report (if you examine the first error message)
that you have not yet provided a ``Natural`` class
that could make the doctest able to succeed.

The Class Itself
----------------

Now we merely have to provide an implementation for our ``Natural`` class.
Create a file ``src/transient/natural.py`` under your Grok instance
and give it the contents:

.. code-block:: python

 class Natural(object):
     """A natural number, here defined as an integer greater than zero."""
 
     def __init__(self, n):
         self.n = abs(int(n)) or 1
 
     def __str__(self):
         return '%d' % self.n
 
     def __repr__(self):
         return 'Natural(%d)' % self.n
 
     @property
     def previous(self):
         if self.n < 2:
             raise AttributeError('There is no natural number less than 1.')
         return Natural(self.n - 1)
 
     @property
     def next(self):
         return Natural(self.n + 1)

     @property
     def factors(self):
         if not hasattr(self, '_factors'):  # compute factors only once!
             n, i = self.n, 2
             self._factors = []
             while i <= n:
                 while n % i == 0:          # while n is divisible by i
                     self._factors.append(Natural(i))
                     n /= i
                 i += 1
         return self._factors

     @property
     def is_prime(self):
         return len(self.factors) < 2

     @property
     def is_composite(self):
	 return len(self.factors) > 1

If you try running ``./bin/test`` again after creating this file,
you should find that the entire ``natural.txt`` docfile
now runs correctly!

I hope that if you are new to Python,
you are not too confused by the code above,
which uses ``@property``
which may not have been covered in the Python tutorial.
But I prefer to show you “real Python” like this,
that reflects how people actually use the language,
rather than artifically simple code
that hides from you the best ways to use Python.
Note that it is *not* necessary to understand ``natural.py``
to enjoy the rest of this tutorial!
Everything we do from this point on
will involve building a framework to use this object on the web;
we will be doing no further development on the class itself.
So all you actually need to understand is how a ``Natural`` behaves,
which was entirely explained in the doctest.

Note that the ``Natural`` class knows nothing about Grok!
This is an important feature of the whole Zope 3 framework,
that bears frequent repeating:
objects are supposed to be simple,
and not have to know that they are being presented on the web.
You should be able to grab objects created anywhere,
from any old library of useful functions you happen to download,
and suit them up to be displayed and manipulated with a browser.
And the ``Natural`` class is exactly like that:
it has no idea that we are about to build a framework around it
that will soon be publishing it on the web.

Having Your View Directly Instantiate An Object
-----------------------------------------------

We now reach the first of our four techniques!

The simplest way to create a transient object for display on the web
involves a technique you may remember from the main Grok tutorial:
providing an ``update()`` method on your View
that creates the object you need
and saves it as an attribute of the View.
As a simple example,
create an ``app.py`` file with these contents:

.. code-block:: python

 import grok
 from transient.natural import Natural

 class TransientApp(grok.Application, grok.Container):
     pass

 class Index(grok.View):
     def update(self):
         self.num = Natural(126)

Do you see what will happen?
Right before Grok renders your View to answer a web request,
Grok will call its ``update()`` method,
and your View will gain an attribute named ``num``
whose value is a new instance of the ``Natural`` class.
This attribute can then be referenced from the page template
corresponding to your view!
Let use write a small page template that accesses the new object.
Try creating an ``/app_templates/index.pt`` file that looks like:

.. code-block:: html

 <html><body>
  <p>
   Behold the number <b tal:content="view/num">x</b>!
   <span tal:condition="view/num/is_prime">It is prime.</span>
   <span tal:condition="view/num/is_composite">Its prime factors are:</span>
  </p>
  <ul tal:condition="view/num/factors">
   <li tal:repeat="factor view/num/factors">
    <b tal:content="factor">f</b>
   </li>
  </ul>
 </body></html>

If you now run your instance
and view the main page of your application,
your browser should show you something like::

 Behold the number 126!  It has several prime factors:

    * 2
    * 3
    * 3
    * 7


You should remember,
when creating an object through an ``update()`` method,
that a new object gets created every time your page is viewed!
This is hard to see with the above example,
of course,
because no matter how many times you hit “reload” on your web browser
you will still see the same number.
So adjust your ``app.py`` file so that it now looks like this:

.. code-block:: python

 import grok, random
 from transient.natural import Natural
 
 class TransientApp(grok.Application, grok.Container):
     pass
 
 class Index(grok.View):
     def update(self):
         self.num = Natural(random.randint(1,1000))

Re-run your application and hit “reload” several times;
each time you should see a different number.

The most important thing to realize when using this method
is that this ``Natural`` object is *not* the object
that Grok is wrapping with the View for display!
The object actually selected by the URL in this example
is your ``TransientApp`` application object itself;
it is this application object which is the ``context`` of the View.
The ``Natural`` object we are creating is nothing more
than an incidental attribute of the View;
it neither has its own URL, nor a View of its own to display it.


Creating Objects Based on Form Input
------------------------------------

What if we wanted the user
to be able to designate which ``Natural`` object was instantiated
for display on this web page?
This is a very common need
when implementing things like a database search form,
where the user's search terms need to be provided as inputs
to the object that will return the search results.

The answer is given in the main Grok tutorial:
if you can write your ``update()`` method
so that it takes keyword parameters,
they will be filled in with any form parameters the user provides.
Rewrite your ``app.py`` to look like:

.. code-block:: python

 import grok, random
 from transient.natural import Natural
 
 class TransientApp(grok.Application, grok.Container):
     pass
 
 class Index(grok.View):
     def update(self, n=None):
         self.badnum = self.num = None
         if n:
             try:
                 self.num = Natural(int(n))
             except:
                 self.badnum = n

And make your ``app_templates/index.pt`` look like:

.. code-block:: html

 <html><body>
  <p tal:condition="view/badnum">This does not look like a natural number:
   &ldquo;<b tal:content="view/badnum">string</b>&rdquo;
  </p>
  <p tal:condition="view/num">
   You asked about the number <b tal:content="view/num">x</b>!<br/>
   <span tal:condition="view/num/is_prime">It is prime.</span>
   <span tal:condition="view/num/is_composite">Its prime factors are:
    <span tal:repeat="factor view/num/factors">
     <b tal:content="factor">f</b
     ><span tal:condition="not:repeat/factor/end">,</span>
    </span>
   </span>
  </p>
  <form tal:attributes="action python:view.url()" method="GET">
   Choose a number: <input type="text" name="n" value="" />
   <input type="submit" value="Go" />
  </form>
 </body></html>

This time, when you restart your Grok instance
and look at your application front page,
you will see a form asking for a number::

 Choose a number: __________  [Go]

Enter a positive integer and submit the form
(try to choose something with less than seven digits
to keep the search for prime factors short),
and you will see something like::

 You asked about the number 48382!
 Its prime factors are: 2, 17, 1423
 Choose a number: __________  [Go]

And if you examine the URL to which the form has delivered you,
you will see that the number you have selected
is part of the URL's query section:

   http://localhost:8080/app/index?n=48382

So none of these numbers get their own URL;
they all live on the page ``/app/index``
and have to be selected by submitting a query to that one page.


Custom Traversers
-----------------

But what about situations
where you want each of your transient objects
to have its own URL on your site?
The answer is that you can create ``grok.Traverser`` objects that,
when the user enters a URL
and Grok tries to find the object which the URL names,
intercept those requests
and return objects of your own design instead.

For our example application ``app``,
let's make each ``Natural`` object live at a URL like::

   http://localhost:8080/app/natural/496

There is nothing magic about the fact that this URL has three parts,
by the way —
the three parts being the application name ``"app"``,
the word ``"natural"``,
and finally the name of the integer ``"496"``.
You should easily be able to figure out
how to adapt the example application below
either to the situation
where you want all the objects to live at your application root
(which would make the URLs look like ``/app/496``),
or where you want URLs to go several levels deeper
(like if you wanted ``/app/numbers/naturals/496``).

The basic rule is that for each slash-separated URL component
(like ``"natural"`` or ``"496"``)
that does not actually name an object in the ZODB,
you have to provide a ``grok.Traverser``.
Make the ``grok.context`` of the Traverser
the object that lives at the previous URL component,
and give your Traverser a ``traverse()`` method
that takes as its argument the next name in the URL
and returns the object itself.
If the name submitted to your traverser
does not name an object,
simply return ``None``;
this is very easy to do,
since ``None`` is the default return value
of a Python function that ends without a ``return`` statement.

So place the following inside your ``app.py`` file:

.. code-block:: python

 import grok
 from transient.natural import Natural

 class TransientApp(grok.Application, grok.Container):
     pass

 class BaseTraverser(grok.Traverser):
     grok.context(TransientApp)
     def traverse(self, name):
         if name == 'natural':
             return NaturalDir()

 class NaturalDir(object):
     pass

 class NaturalTraverser(grok.Traverser):
     grok.context(NaturalDir)
     def traverse(self, name):
         if name.isdigit() and int(name) > 0:
             return Natural(int(name))

 class NaturalIndex(grok.View):
     grok.context(Natural)
     grok.name('index.html')


And you will only need one template to go with this file,
which you should place in ``app_templates/naturalindex.pt``:

.. code-block:: html

 <html><body>
  This is the number <b tal:content="context">x</b>!<br/>
   <span tal:condition="context/is_prime">It is prime.</span>
   <span tal:condition="context/is_composite">Its prime factors are:
    <span tal:repeat="factor context/factors">
     <b tal:content="factor">f</b
     ><span tal:condition="not:repeat/factor/end">,</span>
    </span>
   </span><br>
 </body></html>

Now, if you view the URL ``/app/natural/496`` on your test server,
you should see::

 This is the number 496!
 Its prime factors are: 2, 2, 2, 2, 31

Note that there is no view name after the URL.
That's because we chose to name our View ``index.html``,
which is the default view name in Zope 3.
(With ``grok.Model`` and ``grok.Container`` objects,
by contrast,
the default view selected if none is named is simply ``index``
without the ``.html`` at the end.)
You can always name the view explicitly, though,
so you will find that you can also view the number 496 at::

 http://kenaniah.ten22:8080/app/natural/496/index.html

It's important to realize this because,
if you need to add more views to a transient object,
you of course will have to add them with other names —
and to see the information in those other views,
users (or the links they use) will have to name the views explicitly.

Two final notes:

* In order to make this example brief,
  the application above does not support
  either the user navigating simply to ``/app``,
  nor will it allow them to view ``/app/natural``,
  because we have provided neither our ``TransientApp`` application object
  nor the ``NaturalDir`` stepping-stone with ``grok.View`` objects
  that could let them be displayed.
  You will almost always,
  of course,
  want to provide a welcoming page
  for the top level of your application;
  but it's up to you whether you think it makes sense
  for users to be able to visit the intermediate ``/app/natural``
  URL or not.
  If not,
  then follow the example above
  and simply do not provide a view,
  and everything else will work just fine.

* In order to provide symmetry in the example above,
  neither the ``TransientApp`` object nor the ``NaturalDir`` object
  knows how to send users to the next objects below them.
  Instead, they are both provided with Traversers.
  It turns out,
  I finally admin here at the bottom of the example,
  that this was not necessary!
  Grok objects like a ``grok.Container`` or a ``grok.Model``
  already have enough magic built-in
  that you can put a ``traverse()`` method
  right on the object
  and Grok will find it when trying to resolve a URL.
  This would not have helped our ``NaturalDir`` object,
  of course,
  because it's not a Grok anything;
  but it means that we can technically delete the first Traverser
  and simply declare the first class as:

  .. code-block:: python

   class TransientApp(grok.Application, grok.Container):
       def traverse(self, name):
           if name == 'natural':
               return NaturalDir()

  The reason I did not do this in the actual example above
  is that showing two different ways to traverse in the same example
  seemed a bit excessive!
  I preferred instead to use a single method, twice,
  that is universal and works everywhere,
  rather than by starting off with a technique
  that does not work for most kinds of Python object.


Providing Links To Other Objects
--------------------------------

What if the object you are wrapping
can return other objects to which the user might want to navigate?
Imagine the possibilities:
a filesystem object you are presenting on the web
might be able to return the files inside of it;
a genealogical application might have person objects
that can return their spouse, children, or grandparents.
In the example we are working on here,
a ``Natural`` object can return
both the previous and the next number;
wouldn't it be nice to give the users links to them?

If in a page template
you naively ask your Grok view
for the URL of a transient object,
you will be disappointed.
Grok *does* know the URL of the object
to which the user has just navigated,
because, well, it's just navigated there,
so adding this near the bottom of your ``naturalindex.pt``
should work just fine::

  This page lives at: <b tal:content="python: view.url(context)">url</b><br>

But if you rewrite your template
so that it tries asking for the URL of any other object,
the result will be a minor explosion.
Try adding this to your ``naturalindex.pt`` file::

  Next number: <b tal:content="python: view.url(context.next)">url</b><br>

and try reloading the page.
On the command line,
your application will return the exception::

 TypeError: There isn't enough context to get URL information.
 This is probably due to a bug in setting up location information.

Do you see the problem?
Because this new ``Natural`` object does not live inside of the ZopeDB,
Grok cannot guess the URL at which you intend it to live.
In order to provide this information,
it is best to call a Zope function called ``locate()``
that marks as object as belonging inside of a particular container.
To get the chance to do this magic,
you'll have to avoid calling ``Natural.previous`` and ``Natural.next``
directly from your page template.
Instead,
provide your view with two new properties
that will grab the ``previous`` and ``next`` attributes
off of the ``Natural`` object which is your current context,
and then perform the required modification before returning them:

.. code-block:: python

 class NaturalIndex(grok.View):

     ...

     @property
     def previous(self):
         if getattr(self.context, 'previous', None):
             n = self.context.previous
             traverser = BaseTraverser(grok.getSite(), None)
             parent = traverser.publishTraverse(None, 'natural')
             return zope.location.location.located(n, parent, str(n))
 
     @property
     def next(self):
         n = self.context.next
         traverser = BaseTraverser(grok.getSite(), None)
         parent = traverser.publishTraverse(None, 'natural')
         return zope.location.location.located(n, parent, str(n))


This forces upon your objects
enough information that Zope can determine their URL —
it will believe that they live inside of the object
named by the URL ``/app/natural``
(or whatever other name you use in the ``PublishTraverse`` call).
With the above in place,
you can add these links to the bottom of your ``naturalindex.pt``
and they should work just fine:

.. code-block:: html

  <tal:if tal:condition="view/previous">
   Previous number: <a tal:attributes="href python: view.url(view.previous)"
    tal:content="view/previous">123</a><br>
  </tal:if>
  Next number: <a tal:attributes="href python: view.url(view.next)"
   tal:content="view/next">123</a><br>

This should get easier in a future version of Grok and Zope!


Writing Your Own Container
--------------------------

The above approach, using Traversers, gives Grok
just enough information
to let users visit your objects,
and for you to assign URLs to them.
But there are several features of a normal ``grok.Container``
that are missing —
there is no way for Grok to list or iterate over the objects,
for example,
nor can it ask whether a particular object lives in the container or not.

While taking full advantage of containers
is beyond the scope of this tutorial,
I ought to show you how the above would be accomplished:

.. code-block:: python

 import grok
 from transient.natural import Natural
 from zope.app.container.interfaces import IItemContainer
 from zope.app.container.contained import Contained
 import zope.location.location
 
 class TransientApp(grok.Application, grok.Container):
     pass
 
 class BaseTraverser(grok.Traverser):
     grok.context(TransientApp)
     def traverse(self, name):
         if name == 'natural':
             return NaturalBox()
 
 class NaturalBox(Contained):
     grok.implements(IItemContainer)
     def __getitem__(self, key):
         if key.isdigit() and int(key) > 0:
             n = Natural(int(key))
             return zope.location.location.located(n, self, key)
         else:
             raise KeyError
 
 class NaturalIndex(grok.View):
     grok.context(Natural)
     grok.name('index.html')
 
     @property
     def previous(self):
         if getattr(self.context, 'previous'):
             n = self.context.previous
             parent = self.context.__parent__
             return zope.location.location.located(n, parent, str(n))
 
     @property
     def next(self):
         n = self.context.next
         parent = self.context.__parent__
         return zope.location.location.located(n, parent, str(n))


Note, first, that this is almost identical to the application
we built in the last section;
the ``grok.Application``,
its ``Traverser``,
and the ``NaturalIndex`` are all the same —
and you can leave alone the ``naturalindex.pt`` you wrote as well.

But instead of placing a ``Traverser`` between our ``Application``
and the actual objects we are delivering,
we have created an actual “container”
that follows a more fundamental protocol.
There are a few differences
in even this simple example.

* A container is supposed to act like a Python dictionary,
  so we have overriden the Python operation ``__getitem__``
  instead of providing a ``traverse()`` method.
  This means that other code using the container
  can find objects inside of it using the ``container[key]``
  Python dictionary syntax.

* A Python ``__getitem__`` method
  is required to raise the ``KeyError`` exception
  when someone tries to look up a key
  that does not exist in the container.
  It is *not* sufficient to merely return ``None``,
  like it was in our ``Traverser`` above,
  because, without the exception,
  Python will assume that the key lookup was successful
  and that ``None`` is the value that was found!

* Finally,
  before returning an object from your container,
  you need to call the Zope ``located()`` function
  to make sure the object gets marked up
  with information about where it lives on your site.
  A Grok ``Traverser`` does this for you.

Again,
in most circumstances I can imagine,
you will be happier just using a Traverser
like the third example shows,
and not incurring the slight bit of extra work
necessary to offer a full-fledged container.
But,
in case you ever find yourself
wanting to use a widget or utility
that needs an actual container to process,
I wanted you to have this example available.
