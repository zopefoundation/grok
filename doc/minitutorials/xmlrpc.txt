====================
XML-RPC using Grok
====================

:Author: Kushal Das

What is XML-RPC ?
------------------

From the site (http://xmlrpc.com): it's a spec and a set of implementations
that allow software running on disparate operating systems, running in
different environments to make procedure calls over the Internet.

So, What is Grok?
------------------

From the site: Grok is a web application framework for Python developers. It
is aimed at both beginners and very experienced web developers. Grok has an
emphasis on agile development. Grok is easy and powerful.

Grok accomplishes this by being based on Zope 3, an advanced object-oriented
web framework. While Grok is based on Zope 3, and benefits a lot from it, you
do not need to know Zope at all in order to get productive with Grok. 

So, it is cool, isn't it? :)

Installation
--------------

To install the latest grok, give the following command::

    $ sudo easy_install grokproject

This will download and install grok for you. After this we are ready to rock...

Creating our first project
-----------------------------

Let's create the project named "Foo". For that give the command::

    $ grokproject Foo

This will create a subdirectory in the current directory named "Foo", then it
will download Zope3 and install Grok with that which you can start working
with. It will ask you a few questions like::

    Enter module (Name of a demo Python module placed into the package) ['app.py']:

Press Enter for the default value. Then::

    Enter user (Name of an initial administrator user): grok
    Enter passwd (Password for the initial administrator user): grok

We typed "grok" for both the user and password.

Starting up Zope
--------------------

Switch to the Foo directory, and give the command::

    $ bin/zopectl fg

This will startup Zope for you, you can access it through a web browser 
pointing to http://localhost:8080/ . Then add an application named *foo*.

You can access it by http://localhost:8080/foo, it will show::

    Congratulations!

    Your Grok application is up and running. Edit foo/app_templates/index.pt to
    change this page.

Now we are going to write our xmlrpc stuffs inside it.

XML-RPC class
-----------------

Now you can open the file src/foo/app.py in a text editor. The default is
shown below::

    import grok

    class Foo(grok.Application, grok.Container):
        pass
    
    class Index(grok.View):
        pass # see app_templates/index.pt

We will another class which will be available through this application class,
the new class should inherit ``grok.XMLRPC for this``, and we will write a 
``say()`` method. It will return "Hello World!". So, the changed file::

    import grok

    class Foo(grok.Application, grok.Container):
        pass

    class Index(grok.View):
        pass # see app_templates/index.pt

    class FooXMLRPC(grok.XMLRPC):
        """The methods in this class will be available as XMLRPC methods
           on 'Foo' applications."""

        def say(self):
            return 'Hello world!'

The name of the class doesn't matter, so you can give it any name.
Restart the Zope in the console, and you can connect to it through any xmlrpc
client. Below is an example (fooclient.py)::

    #!/usr/bin/env python
    import xmlrpclib
    
    s = xmlrpclib.Server('http://localhost:8080/foo')
    print s.say()

Run this and see !!

Class in a different file
---------------------------

What if you want to write the class in a different file in the src/foo
directory and still want to have the methods to be available under Foo
application. For that you need to tell grok explicitly that the new class to
associate it to the Foo model by using the grok.context class annotation.

What is a class annotation?
-----------------------------

A class annotation is a declarative way to tell grok something about a Python
class. Let's see the example, we write a Boom.py with a Boom class::

    import grok
    from app import Foo

    class Boom(grok.XMLRPC):
        grok.context(Foo)

        def dance(self):
            return "Boom is dancing!!"

Look at the line where it says ``grok.context(Foo)`` this is doing all the
magic. In the fooclient.py you just need to call ``s.dance()`` instead of 
``s.say()``.

So, now write your dream system...


