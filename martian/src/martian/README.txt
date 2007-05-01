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
is an object that can *grok* objects - execute configuration actions
pertaining to the grokked object, such as registering it with some
central registry. Different kinds of martians can grok different types
of objects (instances, classes, functions).

Let's define a Martian to help us register the file type handler
functions as seen in our previous example::

  >>> import types
  >>> from zope.interface import implements
  >>> from martian import InstanceMartian
  >>> class FileTypeMartian(InstanceMartian):
  ...   component_class = types.FunctionType 
  ...
  ...   def grok(self, name, obj, **kw):
  ...     if not name.startswith('handle_'):
  ...       return False
  ...     ext = name.split('_')[1]
  ...     filehandler.extension_handlers['.' + ext] = obj
  ...     return True

This ``InstanceMartian`` allows us to grok instances of a particular
type (such as functions). We need to define the type of object we're
looking for with the ``component_class`` attribute. In the ``grok``
method, we first make sure we only grok functions that have a name
that starts with ``handle_``. Then we determine the used extension
from the name and register the funcion in the ``extension_handlers``
dictionary of the ``filehandler`` module. We return ``True`` if we
indeed grokked the object.

An instance will provide the IMartian interface::

  >>> filetype_martian = FileTypeMartian()
  >>> from martian.interfaces import IMartian
  >>> IMartian.providedBy(filetype_martian)
  True

Now let's use the martian to grok a new handle function::

  >>> def handle_jpg(filepath):
  ...   return "JPG file"
  >>> filetype_martian.grok('handle_jpg', handle_jpg)
  True

After we grokked, we have have registered a handler for ``.jpg`` files
(the extension to register under was deduced from the function name)::
 
  >>> sorted(filehandler.extension_handlers.keys())
  ['.jpg', '.png', '.txt', '.xml']

This means now our ``filehandler.handle`` function is now able to
handle JPG files as well::
  
  >>> filehandler.handle('image2.jpg')
  'JPG file'

If we try to grok a function that doesn't start with ``handle_`` in its
name, nothing will happen::

  >>> def something(filepath):
  ...   return 'Something'
  >>> filetype_martian.grok('something', something)
  False
  >>> 'something' in filehandler.extension_handlers
  False

Grokking a module
-----------------

Grokking individual components is useful, but to make Martian really
useful we need to be able to grok whole modules or packages as well.
Let's look at a special martian that can grok a Python module::

  >>> from martian import ModuleMartian

The idea is that the ``ModuleMartian`` groks any components in a
module that it recognizes. A ``ModuleMartian`` does not work alone. It
needs to be supplied with one or more martians that can grok the
components to be founded in a module::

  >>> module_martian = ModuleMartian()
  >>> module_martian.register(filetype_martian)

Note that directly putting a martian into a ``ModuleMartian`` is
typically not recommended - normally you would put in a multi martian
(see the examples for multi martians). We can do it here as the only
thing we want to grok are functions and other objects are rejected on
a name basis.

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

Let's grok it::

  >>> module_martian.grok('lotsofhandlers', lotsofhandlers)
  True

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
  True
  >>> filehandler.handle('test.txt')
  'Text file'

InstanceMartian
---------------

We have seen how to grok module-level functions. Let's now grok some
other kind of instance, a ``Color``::

  >>> class color(FakeModule):
  ...   class Color(object):
  ...     def __init__(self, r, g, b):
  ...       self.r = r
  ...       self.g = g
  ...       self.b = b
  ...     def __repr__(self):
  ...       return '<Color %s %s %s>' % (self.r, self.g, self.b) 
  ...   all_colors = {}
  >>> color = fake_import(color)

We now want a martian that can recognize colors and put them in the
``all_colors`` dictionary, with the names as the keys, and the color
object as the values. We can use ``InstanceMartian`` to construct it::

  >>> class ColorMartian(InstanceMartian):
  ...   component_class = color.Color
  ...   def grok(self, name, obj):
  ...     color.all_colors[name] = obj
  ...     return True

Let's create ``color_martian`` and grok a color::

  >>> color_martian = ColorMartian()
  >>> black = color.Color(0, 0, 0) # we DO consider black as a color :)
  >>> color_martian.grok('black', black)
  True

It ends up in the ``all_colors`` dictionary::

  >>> color.all_colors
  {'black': <Color 0 0 0>}

If we put ``color_martian`` into a ``ModuleMartian``, we can now grok
multiple colors in a module::

  >>> Color = color.Color
  >>> class colors(FakeModule):
  ...   red = Color(255, 0, 0)
  ...   green = Color(0, 255, 0)
  ...   blue = Color(0, 0, 255)
  ...   white = Color(255, 255, 255)
  >>> colors = fake_import(colors)
  >>> colors_martian = ModuleMartian() 
  >>> colors_martian.register(color_martian)
  >>> colors_martian.grok('colors', colors)
  True
  >>> sorted(color.all_colors.items())
  [('black', <Color 0 0 0>), 
   ('blue', <Color 0 0 255>), 
   ('green', <Color 0 255 0>), 
   ('red', <Color 255 0 0>), 
   ('white', <Color 255 255 255>)]

Subclasses of ``Color`` are also grokked::

  >>> class subcolors(FakeModule):
  ...   class SpecialColor(Color):
  ...     pass
  ...   octarine = SpecialColor(-255, 0, -255)
  >>> subcolors = fake_import(subcolors)
  >>> colors_martian.grok('subcolors', subcolors)
  True
  >>> 'octarine' in color.all_colors
  True

MultiInstanceMartian
--------------------

In the previous section we have created a particular martian that
looks for instances of a component class, in this case
``Color``. Let's introduce another ``InstanceMartian`` that looks for
instances of ``Sound``::
  
  >>> class sound(FakeModule):
  ...   class Sound(object):
  ...     def __init__(self, desc):
  ...       self.desc = desc
  ...     def __repr__(self):
  ...       return '<Sound %s>' % (self.desc) 
  ...   all_sounds = {}
  >>> sound = fake_import(sound)

  >>> class SoundMartian(InstanceMartian):
  ...   component_class = sound.Sound
  ...   def grok(self, name, obj):
  ...     sound.all_sounds[name] = obj
  ...     return True
  >>> sound_martian = SoundMartian()
 
What if we now want to look for ``Sound`` and ``Color`` instances at
the same time? We have to use the ``color_martian`` and
``sound_martian`` at the same time, and we can do this with a
``MultiInstanceMartian``::

  >>> from martian.core import MultiInstanceMartian
  >>> multi_martian = MultiInstanceMartian()
  >>> multi_martian.register(color_martian)
  >>> multi_martian.register(sound_martian)

Let's grok a new color with our ``multi_martian``::

  >>> grey = Color(100, 100, 100)
  >>> multi_martian.grok('grey', grey)
  True
  >>> 'grey' in color.all_colors
  True

Let's grok a sound with our ``multi_martian``::
  
  >>> moo = sound.Sound('Moo!')
  >>> multi_martian.grok('moo', moo)
  True
  >>> 'moo' in sound.all_sounds
  True

We can also grok other objects, but this will have no effect::

  >>> something_else = object()
  >>> multi_martian.grok('something_else', something_else)
  False

Let's put our ``multi_martian`` in a ``ModuleMartian``. We can do
this by passing it explicitly to the ``ModuleMartian`` factory::

  >>> module_martian = ModuleMartian(multi_martian)

We can now grok a module for both ``Color`` and ``Sound`` instances::

  >>> Sound = sound.Sound
  >>> class lightandsound(FakeModule):
  ...   dark_red = Color(150, 0, 0)
  ...   scream = Sound('scream')
  ...   dark_green = Color(0, 150, 0)
  ...   cheer = Sound('cheer')
  >>> lightandsound = fake_import(lightandsound)
  >>> module_martian.grok('lightandsound', lightandsound)
  True
  >>> 'dark_red' in color.all_colors
  True
  >>> 'dark_green' in color.all_colors
  True
  >>> 'scream' in sound.all_sounds
  True
  >>> 'cheer' in sound.all_sounds
  True

ClassMartian
------------

Besides instances we can also grok classes. Let's define an application
where we register classes representing animals::

  >>> class animal(FakeModule):
  ...   class Animal(object):
  ...     name = None
  ...     def __repr__(self):
  ...       return '<Animal %s>' % self.name
  ...   all_animals = {}
  ...   def create_animal(name):
  ...     return all_animals[name]() 
  >>> animal = fake_import(animal)
  
Let's define a martian that can grok an ``Animal``::

  >>> from martian import ClassMartian
  >>> class AnimalMartian(ClassMartian):
  ...   component_class = animal.Animal
  ...   def grok(self, name, obj, **kw):
  ...     animal.all_animals[obj.name] = obj
  ...     return True

Let's test our martian::

  >>> animal_martian = AnimalMartian()
  >>> class Snake(animal.Animal):
  ...   name = 'snake'
  >>> animal_martian.grok('snake', Snake)
  True
  >>> animal.all_animals.keys()
  ['snake']

We can create a snake now::

  >>> animal.create_animal('snake')
  <Animal snake>

MultiClassMartian
-----------------

We now want to be able to grok the following module and have the
``Animal`` subclasses (but not the ``Chair`` class, which is not an
animal) automatically become available::

  >>> class animals(FakeModule):
  ...   class Elephant(animal.Animal):
  ...     name = 'elephant'
  ...   class Tiger(animal.Animal):
  ...     name = 'tiger'
  ...   class Lion(animal.Animal):
  ...     name = 'lion'
  ...   class Chair(object):
  ...     name = 'chair'
  >>> animals = fake_import(animals)

First we need to wrap our ``AnimalMartian`` into a ``MultiClassMartian``::

 >>> from martian.core import MultiClassMartian
 >>> multi_martian = MultiClassMartian()
 >>> multi_martian.register(animal_martian)

Now let's wrap it into a ``ModuleMartian`` and grok the module::

  >>> martian = ModuleMartian(multi_martian)
  >>> martian.grok('animals', animals)
  True

The animals (but not anything else) should have become available::

  >>> sorted(animal.all_animals.keys())
  ['elephant', 'lion', 'snake', 'tiger']

We can create animals using their name now::

  >>> animal.create_animal('elephant')
  <Animal elephant>
  >>> animal.create_animal('tiger')
  <Animal tiger>

MultiMartian
------------

``MultiInstanceMartian`` and ``MultiClassMartian`` can grok instances
and classes respectively, but a ``MultiInstanceMartian`` won't work
correctly if it runs into a class and vice versa. For that we use a
``MultiMartian``, which can deal with the full range of objects that
can be grokked, and skips those it doesn't recognize.

Let's fill a ``MultiMartian`` with a bunch of martians::

  >>> from martian import MultiMartian
  >>> multi = MultiMartian()
  >>> multi.register(filetype_martian)
  >>> multi.register(color_martian)
  >>> multi.register(sound_martian)
  >>> multi.register(animal_martian)

Let's try it with some individual objects::

  >>> class Whale(animal.Animal):
  ...    name = 'whale'
  >>> multi.grok('Whale', Whale)
  True
  >>> 'whale' in animal.all_animals
  True
 
This should have no effect, but not fail::

  >>> my_whale = Whale()
  >>> multi.grok('my_whale', my_whale)
  False

Grokked by the ColorMartian::

  >>> multi.grok('dark_grey', Color(50, 50, 50))
  True
  >>> 'dark_grey' in color.all_colors 
  True

Grokked by the SoundMartian::
  
  >>> multi.grok('music', Sound('music'))
  True
  >>> 'music' in sound.all_sounds
  True

Not grokked::

  >>> class RockMusic(Sound):
  ...   pass
  >>> multi.grok('RockMusic', RockMusic)
  False

Grokked by SoundMartian::

  >>> multi.grok('rocknroll', RockMusic('rock n roll'))
  True
  >>> 'rocknroll' in sound.all_sounds
  True

Not grokked::

  >>> class Chair(object):
  ...   pass
  >>> multi.grok('Chair', Chair)
  False

Grokked by ``filetype_martian``::

  >>> def handle_py(filepath):
  ...   return "Python file"
  >>> multi.grok('handle_py', handle_py)
  True
  >>> '.py' in filehandler.extension_handlers
  True

Not grokked:

  >>> def foo():
  ...   pass
  >>> multi.grok('foo', foo)
  False

Not grokked either::
  
  >>> another = object()
  >>> multi.grok('another', another)
  False
  
Let's make a module which has a mixture between classes and instances,
some of which can be grokked::

  >>> class mix(FakeModule):
  ...   # grokked by AnimalMartian
  ...   class Whale(animal.Animal):
  ...      name = 'whale'
  ...   # not grokked
  ...   my_whale = Whale()
  ...   # grokked by ColorMartian
  ...   dark_grey = Color(50, 50, 50)
  ...   # grokked by SoundMartian
  ...   music = Sound('music')
  ...   # not grokked
  ...   class RockMusic(Sound):
  ...      pass
  ...   # grokked by SoundMartian
  ...   rocknroll = RockMusic('rock n roll')
  ...   # grokked by AnimalMartian
  ...   class Dragon(animal.Animal):
  ...     name = 'dragon'
  ...   # not grokked
  ...   class Chair(object):
  ...     pass
  ...   # grokked by filetype_martian
  ...   def handle_py(filepath):
  ...     return "Python file"
  ...   # not grokked
  ...   def foo():
  ...     pass
  ...   # grokked by AnimalMartian
  ...   class SpermWhale(Whale):
  ...     name = 'sperm whale'
  ...   # not grokked
  ...   another = object()
  >>> mix = fake_import(mix)

Let's construct a ``ModuleMartian`` that can grok this module::

  >>> mix_martian = ModuleMartian(multi)

Note that this is actually equivalent to calling ``ModuleMartian``
without arguments and then calling ``register`` for the individual
``ClassMartian`` and ``InstanceMartian`` objects.

Before we do the grokking, let's clean up our registration
dictionaries::

  >>> filehandler.extension_handlers = {}
  >>> color.all_colors = {} 
  >>> sound.all_sounds = {}
  >>> animal.all_animals = {}

Now we grok::

  >>> mix_martian.grok('mix', mix)
  True
  >>> sorted(filehandler.extension_handlers.keys())
  ['.py']
  >>> sorted(color.all_colors.keys())
  ['dark_grey']
  >>> sorted(sound.all_sounds.keys())
  ['music', 'rocknroll']
  >>> sorted(animal.all_animals.keys())
  ['dragon', 'sperm whale', 'whale']

GlobalMartian
-------------

Sometimes you want to let a grok action happen for each module. The
grok action could for instance read the globals of a module, or even
static files associated with the module by name. Let's create a module
with some global value::

  >>> class g(FakeModule):
  ...   amount = 50
  >>> g = fake_import(g)
 
Now let's create a ``GlobalMartian`` that reads ``amount`` and stores
it in the ``read_amount`` dictionary::

  >>> read_amount = {}
  >>> from martian import GlobalMartian
  >>> class AmountMartian(GlobalMartian):
  ...   def grok(self, name, module):
  ...     read_amount[None] = module.amount
  ...     return True

Let's construct a ``ModuleMartian`` with this ``GlobalMartian`` registered::

  >>> martian = ModuleMartian()
  >>> martian.register(AmountMartian())

Now we grok and should pick up the right value::

  >>> martian.grok('g', g)
  True
  >>> read_amount[None]
  50 

Old-style class support
-----------------------

So far we have only grokked either new-style classes or instances of
new-style classes. It is also possible to grok old-style classes and
their instances::

  >>> class oldstyle(FakeModule):
  ...   class Machine:
  ...     pass
  ...   all_machines = {}
  ...   all_machine_instances = {}
  >>> oldstyle = fake_import(oldstyle)

Let's make a martian for the old style class::

  >>> class MachineMartian(ClassMartian):
  ...   component_class = oldstyle.Machine
  ...   def grok(self, name, obj):
  ...     oldstyle.all_machines[name] = obj
  ...     return True

And another martian for old style instances::

  >>> class MachineInstanceMartian(InstanceMartian):
  ...   component_class = oldstyle.Machine
  ...   def grok(self, name, obj):
  ...     oldstyle.all_machine_instances[name] = obj
  ...     return True

The multi martian should succesfully grok the old-style ``Machine`` class
and instances of it::

  >>> multi = MultiMartian()
  >>> multi.register(MachineMartian())
  >>> multi.register(MachineInstanceMartian())
  >>> class Robot(oldstyle.Machine):
  ...   pass
  >>> multi.grok('Robot', Robot)
  True
  >>> oldstyle.all_machines.keys()
  ['Robot']
  >>> robot = Robot()
  >>> multi.grok('robot', robot)
  True
  >>> oldstyle.all_machine_instances.keys()
  ['robot']
