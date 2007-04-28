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

The ``martian`` package is a spin-off from the `Grok project`_. In
Grok, as well as in the ``martian`` package, "grokking" stands for the
process of deducing declarative configuration actions from Python
code.

In the novel, grokking is originally a concept that comes from the
planet Mars. Martians *grok*. Since this package helps you grok code,
it's a Martian.

.. _`Grok project`: http://grok.zope.org

Motivation
----------

What does all this mean? In order to explain this, let's first look at
an example of a simple framework that can be *configured* with
plugins. We will define a framework for handling files based on their
extensions::

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

Since normally we cannot create modules in a doctest, we will emulate
Python modules using the ``FakeModule`` class. Whenever you see
``FakeModule`` subclasses, imagine you're looking at a module
definition. We also need to be able to import our fake module, so we
also have a fake import statement that lets us do this::

  >>> filehandler = fake_import(filehandler)

Now let's try the ``handle_file`` function for a few file types::

  >>> filehandler.handle('test.txt')
  'Text file'
  >>> filehandler.handle('test2.xml')
  'XML file'

File extensions that we do not recognize give us a KeyError::
 
  >>> filehandler.handle('image.png')  
  Traceback (most recent call last):
  ...
  KeyError: '.png'

What about pluggability? We want to plug into this filehandler
framework and provide the a handler for ``.png`` files. Since we are
writing a plugin, we cannot change the ``filehandler`` module
directly. Let's write an extension module instead::

  >>> class pnghandler(FakeModule):
  ...    def handle_png(filepath):
  ...        return "PNG file"
  ...
  ...    filehandler.extension_handlers['.png'] = handle_png
  >>> pnghandler = fake_import(pnghandler)

PNG handling works now::

  >>> filehandler.handle('image.png')
  'PNG file'

The action of registering something into a central registry is also
called *configuration*. Larger frameworks often offer a lot of ways to
configure them: ways to combine its own components along with
components you provide to build a larger application. Using Python
code to manually hook components into registries can get rather
cumbersome and poses a maintenance risk. It is tempting to start doing
fancy things in Python code such as conditional configuration, making
the configuration state of a program hard to understand. Doing
configuration at import time can also lead to unwanted side effects
during import and ordering problems.

Martian provides a framework that allows configuration to be expressed
in declarative Python code. The idea is to make these declarations so
minimal and easy to read that even complex and extensive configuration
does not overly burden the programmer or the person reading the code.
Configuration actions are also executed during a separate phase ("grok
time"), not at import time.

Martians that grok
------------------

What is a ``Martian``? It is an object that can grok other objects -
execute configuration actions pertaining to the other
object. Different kinds of Martians can grok different types of
objects.

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

This martian will provide the IMartian interface::

  >>> filetype_martian = FileTypeMartian()
  >>> from martian.interfaces import IMartian
  >>> IMartian.providedBy(filetype_martian)
  True

The martian will only match function objects that have a name
that starts with ``'handle_'``::

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

Grokking will have have registered a handler for ``.jpg`` files (deducing
the extension to register under from the function name)::
 
  >>> sorted(filehandler.extension_handlers.keys())
  ['.jpg', '.png', '.txt', '.xml']

This means now our ``filehandler.handle`` function is now able to
handle JPG files as well::
  
  >>> filehandler.handle('image2.jpg')
  'JPG file'

Grokking a module
-----------------

Let's now look at a special martian that can grok a Python
module::

  >>> from martian import ModuleMartian
  >>> module_martian = ModuleMartian()
  
The idea is that the ``ModuleMartian`` groks any components in a
module that it recognizes. A ModuleMartian does not work alone. It
needs to be supplied with one or more martians that can grok
components to be found in a module. Let's register the
``filetype_martian`` with our ``module_martian``::

  >>> module_martian.register(filetype_martian)

We define a module that defines a lot of filetype handlers to be
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

As you can see, we can now define handlers without ever having to
register them manually. We can now rewrite our original module and
take out the manual registrations completely::

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
