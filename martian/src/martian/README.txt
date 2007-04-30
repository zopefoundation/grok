Martian
=======

"There was so much to grok, so little to grok from." -- Stranger in a
Strange Land, by Robert A. Heinlein

Martian provides infrastructure for declarative configuration of
Python code. Martian is especially useful for the construction of
frameworks that need to provide a flexible plugin infrastructure. 

Why is this package named ``martian``? In the novel "Stranger in a
Strange Land", the verb *grok* is introduced:

  Grok means to understand so thoroughly that the observer becomes a
  part of the observed -- to merge, blend, intermarry, lose identity
  in group experience.

In the context of this package, "grokking" stands for the process of
deducing declarative configuration actions from Python code. In the
novel, grokking is originally a concept that comes from the planet
Mars. Martians *grok*. Since this package helps you grok code, it's
called Martian.

The ``martian`` package is a spin-off from the `Grok project`_, in the
context of which this codebase was first developed. While Grok uses
it, the code is completely independent of Grok.

.. _`Grok project`: http://grok.zope.org

Motivation
----------

"Deducing declarative configuration actions from Python code" - that
sounds very abstracxt. What does it actually mean? In order to explain
this, let's first look at an example of a simple framework that can be
*configured* with plugins. We will define a framework for handling
files based on their extensions::

  >>> class filehandler(FakeModule):
  ...   import os
  ...
  ...   def handle_txt(filepath):
  ...     return "Text file"
  ...
  ...   def handle_xml(filepath):
  ...     return "XML file"
  ...
  ...   extension_handlers = { '.txt': handle_txt, '.xml': handle_xml }
  ...
  ...   def handle(filepath):
  ...      name, ext = os.path.splitext(filepath)
  ...      return extension_handlers[ext](filepath)

Since normally we cannot create modules in a doctest, we have emulated
the ``filehandler`` Python module using the ``FakeModule``
class. Whenever you see ``FakeModule`` subclasses, imagine you're
looking at a module definition in a ``.py`` file. Now that we have
defined a module ``filehandler, we also need to be able to import
it. To do so we can use a a fake import statement that lets us do
this::

  >>> filehandler = fake_import(filehandler)

Now let's try the ``handle`` function for a few file types::

  >>> filehandler.handle('test.txt')
  'Text file'
  >>> filehandler.handle('test2.xml')
  'XML file'

File extensions that we do not recognize cause a ``KeyError`` to be
raisedr::
 
  >>> filehandler.handle('image.png')  
  Traceback (most recent call last):
  ...
  KeyError: '.png'

We now want to plug into this filehandler framework and provide the a
handler for ``.png`` files. Since we are writing a plugin, we cannot
change the ``filehandler`` module directly. Let's write an extension
module instead::

  >>> class pnghandler(FakeModule):
  ...    def handle_png(filepath):
  ...        return "PNG file"
  ...
  ...    filehandler.extension_handlers['.png'] = handle_png
  >>> pnghandler = fake_import(pnghandler)

In the extension module, we manipulate the ``extension_handlers``
dictionary of the ``filehandler`` module and plug in our own
function. PNG handling works now::

  >>> filehandler.handle('image.png')
  'PNG file'

The action of registering something into a central registry is also
called *configuration*. Larger frameworks often offer a lot of points
where you can configure them: ways to combine its own components with
components you provide yourself to build a larger application. 

Above we plug into our ``extension_handler`` registry using Python
code. Using separate code to manually hook components into registries
can get rather cumbersome - each time you write an extension, you also
need to remember you need to register it. It also poses a maintenance
risk. It is tempting to start doing fancy things in Python code such
as conditional configuration, making the configuration state of a
program hard to understand. Another problem is that doing
configuration at import time can also lead to unwanted side effects
during import and ordering problems. It can also make code harder to
test.

Martian provides a framework that allows configuration to be expressed
in declarative Python code. These declarations can often be decuded
from the structure of the code itself. The idea is to make these
declarations so minimal and easy to read that even extensive
configuration does not overly burden the programmers working with the
code. Configuration actions are executed during a separate phase
("grok time"), not at import time, which makes it easier to reason
about and easier to test.

Martians that grok
------------------

In this section we define the concept of a ``Martian``. A ``Martian``
is an object that can *grok* other objects - execute configuration
actions pertaining to the other object, such as registering it with
some central registry. Different kinds of Martians can grok different
types of objects.

Let's define a Martian to help us register the file type handler
functions as seen in our previous example::

  >>> import types
  >>> from zope.interface import implements
  >>> from martian import InstanceMartian
  >>> class FileTypeMartian(InstanceMartian):
  ...   component_class = types.FunctionType 
  ...   def match(self, name, obj):
  ...     return (super(FileTypeMartian, self).match(name, obj) and 
  ...             name.startswith('handle_'))
  ...
  ...   def grok(self, name, obj, **kw):
  ...       ext = name.split('_')[1]
  ...       filehandler.extension_handlers['.' + ext] = obj


This ``InstanceMartian`` allows us to grok instances of a particular
type (such as functions). We need to define the type of object we're
looking for with the ``component_class`` attribute. In addition, we've
amended the ``match`` method to make sure we only match those
instances that have a name that starts with ``handle_`.

An instance will provide the IMartian interface::

  >>> filetype_martian = FileTypeMartian()
  >>> from martian.interfaces import IMartian
  >>> IMartian.providedBy(filetype_martian)
  True

The martian will match function objects that have a name that starts
with ``'handle_'``::

  >>> filetype_martian.match('handle_txt', filehandler.handle_txt)
  True
  >>> filetype_martian.match('handle_xml', filehandler.handle_xml)
  True
  >>> filetype_martian.match('handle_png', pnghandler.handle_png)
  True

It won't match ``handle``, as that does not start with ``handle_``::

  >>> filetype_martian.match('handle', filehandler.handle)
  False

It also won't match non-function objects that happen to be prefixed
with ``handle_``::

  >>> class handle_foo(object):
  ...   pass
  >>> filetype_martian.match('handle_foo', handle_foo)
  False
  >>> filetype_martian.match('handle_foo', handle_foo())
  False

Now let's use the martian to grok a new handle function::

  >>> def handle_jpg(filepath):
  ...   return "JPG file"
  >>> filetype_martian.match('handle_jpg', handle_jpg)
  True
  >>> filetype_martian.grok('handle_jpg', handle_jpg)

After we grokked, we have have registered a handler for ``.jpg`` files
(the extension to register under was deduced from the function name)::
 
  >>> sorted(filehandler.extension_handlers.keys())
  ['.jpg', '.png', '.txt', '.xml']

This means now our ``filehandler.handle`` function is now able to
handle JPG files as well::
  
  >>> filehandler.handle('image2.jpg')
  'JPG file'

Grokking a module
-----------------

Grokking individual components is useful, but to make Martian really
useful we need to be able to grok whole modules or packages as well.
Let's look at a special martian that can grok a Python module::

  >>> from martian import ModuleMartian
  >>> module_martian = ModuleMartian()

The idea is that the ``ModuleMartian`` groks any components in a
module that it recognizes. A ``ModuleMartian`` does not work alone. It
needs to be supplied with one or more martians that can grok
components to be found in a module. Let's register the
``filetype_martian`` with our ``module_martian``::

  >>> module_martian.register(filetype_martian)

We now define a module that defines a few filetype handlers to be
grokked::

  >>> class lotsofhandlers(FakeModule):
  ...   def handle_exe(filepath):
  ...     return "EXE file"
  ...
  ...   def handle_ogg(filepath):
  ...     return "OGG file"
  ...
  ...   def handle_svg(filepath):
  ...     return "SVG file"
  >>> lotsofhandlers = fake_import(lotsofhandlers)

Our module martian matches this module::

  >>> module_martian.match('lotsofhandlers', lotsofhandlers)
  True

Let's grok it::

  >>> module_martian.grok('lotsofhandlers', lotsofhandlers)

The new registrations are now available::

  >>> sorted(filehandler.extension_handlers.keys())
  ['.exe', '.jpg', '.ogg', '.png', '.svg', '.txt', '.xml']

The system indeed recognizes them now::

  >>> filehandler.handle('test.ogg')
  'OGG file'
  >>> filehandler.handle('test.svg')
  'SVG file'
  >>> filehandler.handle('test.exe')
  'EXE file'

As you can see, with Martian we can now define handlers without ever
having to register them manually. This allows us to rewrite our
original module and take out the manual registrations completely::

  >>> class filehandler(FakeModule):
  ...   import os
  ...
  ...   def handle_txt(filepath):
  ...     return "Text file"
  ...
  ...   def handle_xml(filepath):
  ...     return "XML file"
  ...
  ...   extension_handlers = {}
  ...
  ...   def handle(filepath):
  ...      name, ext = os.path.splitext(filepath)
  ...      return extension_handlers[ext](filepath)

  >>> filehandler = fake_import(filehandler)
 
Let's use martian to do the registrations for us::

  >>> module_martian.grok('filehandler', filehandler)
  >>> filehandler.handle('test.txt')
  'Text file'
