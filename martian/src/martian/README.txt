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

Grokkers that grok
------------------

In this section we define the concept of a ``Grokker``. A ``Grokker``
is an object that can *grok* objects - execute configuration actions
pertaining to the grokked object, such as registering it with some
central registry. Different kinds of grokkers can grok different types
of objects (instances, classes, functions).

Let's define a Grokker to help us register the file type handler
functions as seen in our previous example::

  >>> import types
  >>> from zope.interface import implements
  >>> from martian import InstanceGrokker
  >>> class FileTypeGrokker(InstanceGrokker):
  ...   component_class = types.FunctionType 
  ...
  ...   def grok(self, name, obj, **kw):
  ...     if not name.startswith('handle_'):
  ...       return False
  ...     ext = name.split('_')[1]
  ...     filehandler.extension_handlers['.' + ext] = obj
  ...     return True

This ``InstanceGrokker`` allows us to grok instances of a particular
type (such as functions). We need to define the type of object we're
looking for with the ``component_class`` attribute. In the ``grok``
method, we first make sure we only grok functions that have a name
that starts with ``handle_``. Then we determine the used extension
from the name and register the funcion in the ``extension_handlers``
dictionary of the ``filehandler`` module. We return ``True`` if we
indeed grokked the object.

An instance will provide the IGrokker interface::

  >>> filetype_grokker = FileTypeGrokker()
  >>> from martian.interfaces import IGrokker
  >>> IGrokker.providedBy(filetype_grokker)
  True

Now let's use the grokker to grok a new handle function::

  >>> def handle_jpg(filepath):
  ...   return "JPG file"
  >>> filetype_grokker.grok('handle_jpg', handle_jpg)
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
  >>> filetype_grokker.grok('something', something)
  False
  >>> 'something' in filehandler.extension_handlers
  False

Grokking a module
-----------------

Grokking individual components is useful, but to make Martian really
useful we need to be able to grok whole modules or packages as well.
Let's look at a special grokker that can grok a Python module::

  >>> from martian import ModuleGrokker

The idea is that the ``ModuleGrokker`` groks any components in a
module that it recognizes. A ``ModuleGrokker`` does not work alone. It
needs to be supplied with one or more grokkers that can grok the
components to be founded in a module::

  >>> module_grokker = ModuleGrokker()
  >>> module_grokker.register(filetype_grokker)

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

  >>> module_grokker.grok('lotsofhandlers', lotsofhandlers)
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

  >>> module_grokker.grok('filehandler', filehandler)
  True
  >>> filehandler.handle('test.txt')
  'Text file'

InstanceGrokker
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

We now want a grokker that can recognize colors and put them in the
``all_colors`` dictionary, with the names as the keys, and the color
object as the values. We can use ``InstanceGrokker`` to construct it::

  >>> class ColorGrokker(InstanceGrokker):
  ...   component_class = color.Color
  ...   def grok(self, name, obj):
  ...     color.all_colors[name] = obj
  ...     return True

Let's create ``color_grokker`` and grok a color::

  >>> color_grokker = ColorGrokker()
  >>> black = color.Color(0, 0, 0) # we DO consider black as a color :)
  >>> color_grokker.grok('black', black)
  True

It ends up in the ``all_colors`` dictionary::

  >>> color.all_colors
  {'black': <Color 0 0 0>}

If we put ``color_grokker`` into a ``ModuleGrokker``, we can now grok
multiple colors in a module::

  >>> Color = color.Color
  >>> class colors(FakeModule):
  ...   red = Color(255, 0, 0)
  ...   green = Color(0, 255, 0)
  ...   blue = Color(0, 0, 255)
  ...   white = Color(255, 255, 255)
  >>> colors = fake_import(colors)
  >>> colors_grokker = ModuleGrokker() 
  >>> colors_grokker.register(color_grokker)
  >>> colors_grokker.grok('colors', colors)
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
  >>> colors_grokker.grok('subcolors', subcolors)
  True
  >>> 'octarine' in color.all_colors
  True

MultiInstanceGrokker
--------------------

In the previous section we have created a particular grokker that
looks for instances of a component class, in this case
``Color``. Let's introduce another ``InstanceGrokker`` that looks for
instances of ``Sound``::
  
  >>> class sound(FakeModule):
  ...   class Sound(object):
  ...     def __init__(self, desc):
  ...       self.desc = desc
  ...     def __repr__(self):
  ...       return '<Sound %s>' % (self.desc) 
  ...   all_sounds = {}
  >>> sound = fake_import(sound)

  >>> class SoundGrokker(InstanceGrokker):
  ...   component_class = sound.Sound
  ...   def grok(self, name, obj):
  ...     sound.all_sounds[name] = obj
  ...     return True
  >>> sound_grokker = SoundGrokker()
 
What if we now want to look for ``Sound`` and ``Color`` instances at
the same time? We have to use the ``color_grokker`` and
``sound_grokker`` at the same time, and we can do this with a
``MultiInstanceGrokker``::

  >>> from martian.core import MultiInstanceGrokker
  >>> multi_grokker = MultiInstanceGrokker()
  >>> multi_grokker.register(color_grokker)
  >>> multi_grokker.register(sound_grokker)

Let's grok a new color with our ``multi_grokker``::

  >>> grey = Color(100, 100, 100)
  >>> multi_grokker.grok('grey', grey)
  True
  >>> 'grey' in color.all_colors
  True

Let's grok a sound with our ``multi_grokker``::
  
  >>> moo = sound.Sound('Moo!')
  >>> multi_grokker.grok('moo', moo)
  True
  >>> 'moo' in sound.all_sounds
  True

We can also grok other objects, but this will have no effect::

  >>> something_else = object()
  >>> multi_grokker.grok('something_else', something_else)
  False

Let's put our ``multi_grokker`` in a ``ModuleGrokker``. We can do
this by passing it explicitly to the ``ModuleGrokker`` factory::

  >>> module_grokker = ModuleGrokker(grokker=multi_grokker)

We can now grok a module for both ``Color`` and ``Sound`` instances::

  >>> Sound = sound.Sound
  >>> class lightandsound(FakeModule):
  ...   dark_red = Color(150, 0, 0)
  ...   scream = Sound('scream')
  ...   dark_green = Color(0, 150, 0)
  ...   cheer = Sound('cheer')
  >>> lightandsound = fake_import(lightandsound)
  >>> module_grokker.grok('lightandsound', lightandsound)
  True
  >>> 'dark_red' in color.all_colors
  True
  >>> 'dark_green' in color.all_colors
  True
  >>> 'scream' in sound.all_sounds
  True
  >>> 'cheer' in sound.all_sounds
  True

ClassGrokker
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
  
Let's define a grokker that can grok an ``Animal``::

  >>> from martian import ClassGrokker
  >>> class AnimalGrokker(ClassGrokker):
  ...   component_class = animal.Animal
  ...   def grok(self, name, obj, **kw):
  ...     animal.all_animals[obj.name] = obj
  ...     return True

Let's test our grokker::

  >>> animal_grokker = AnimalGrokker()
  >>> class Snake(animal.Animal):
  ...   name = 'snake'
  >>> animal_grokker.grok('snake', Snake)
  True
  >>> animal.all_animals.keys()
  ['snake']

We can create a snake now::

  >>> animal.create_animal('snake')
  <Animal snake>

MultiClassGrokker
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

First we need to wrap our ``AnimalGrokker`` into a ``MultiClassGrokker``::

 >>> from martian.core import MultiClassGrokker
 >>> multi_grokker = MultiClassGrokker()
 >>> multi_grokker.register(animal_grokker)

Now let's wrap it into a ``ModuleGrokker`` and grok the module::

  >>> grokker = ModuleGrokker(grokker=multi_grokker)
  >>> grokker.grok('animals', animals)
  True

The animals (but not anything else) should have become available::

  >>> sorted(animal.all_animals.keys())
  ['elephant', 'lion', 'snake', 'tiger']

We can create animals using their name now::

  >>> animal.create_animal('elephant')
  <Animal elephant>
  >>> animal.create_animal('tiger')
  <Animal tiger>

MultiGrokker
------------

``MultiInstanceGrokker`` and ``MultiClassGrokker`` can grok instances
and classes respectively, but a ``MultiInstanceGrokker`` won't work
correctly if it runs into a class and vice versa. For that we use a
``MultiGrokker``, which can deal with the full range of objects that
can be grokked, and skips those it doesn't recognize.

Let's fill a ``MultiGrokker`` with a bunch of grokkers::

  >>> from martian import MultiGrokker
  >>> multi = MultiGrokker()
  >>> multi.register(filetype_grokker)
  >>> multi.register(color_grokker)
  >>> multi.register(sound_grokker)
  >>> multi.register(animal_grokker)

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

Grokked by the ColorGrokker::

  >>> multi.grok('dark_grey', Color(50, 50, 50))
  True
  >>> 'dark_grey' in color.all_colors 
  True

Grokked by the SoundGrokker::
  
  >>> multi.grok('music', Sound('music'))
  True
  >>> 'music' in sound.all_sounds
  True

Not grokked::

  >>> class RockMusic(Sound):
  ...   pass
  >>> multi.grok('RockMusic', RockMusic)
  False

Grokked by SoundGrokker::

  >>> multi.grok('rocknroll', RockMusic('rock n roll'))
  True
  >>> 'rocknroll' in sound.all_sounds
  True

Not grokked::

  >>> class Chair(object):
  ...   pass
  >>> multi.grok('Chair', Chair)
  False

Grokked by ``filetype_grokker``::

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
  ...   # grokked by AnimalGrokker
  ...   class Whale(animal.Animal):
  ...      name = 'whale'
  ...   # not grokked
  ...   my_whale = Whale()
  ...   # grokked by ColorGrokker
  ...   dark_grey = Color(50, 50, 50)
  ...   # grokked by SoundGrokker
  ...   music = Sound('music')
  ...   # not grokked
  ...   class RockMusic(Sound):
  ...      pass
  ...   # grokked by SoundGrokker
  ...   rocknroll = RockMusic('rock n roll')
  ...   # grokked by AnimalGrokker
  ...   class Dragon(animal.Animal):
  ...     name = 'dragon'
  ...   # not grokked
  ...   class Chair(object):
  ...     pass
  ...   # grokked by filetype_grokker
  ...   def handle_py(filepath):
  ...     return "Python file"
  ...   # not grokked
  ...   def foo():
  ...     pass
  ...   # grokked by AnimalGrokker
  ...   class SpermWhale(Whale):
  ...     name = 'sperm whale'
  ...   # not grokked
  ...   another = object()
  >>> mix = fake_import(mix)

Let's construct a ``ModuleGrokker`` that can grok this module::

  >>> mix_grokker = ModuleGrokker(grokker=multi)

Note that this is actually equivalent to calling ``ModuleGrokker``
without arguments and then calling ``register`` for the individual
``ClassGrokker`` and ``InstanceGrokker`` objects.

Before we do the grokking, let's clean up our registration
dictionaries::

  >>> filehandler.extension_handlers = {}
  >>> color.all_colors = {} 
  >>> sound.all_sounds = {}
  >>> animal.all_animals = {}

Now we grok::

  >>> mix_grokker.grok('mix', mix)
  True
  >>> sorted(filehandler.extension_handlers.keys())
  ['.py']
  >>> sorted(color.all_colors.keys())
  ['dark_grey']
  >>> sorted(sound.all_sounds.keys())
  ['music', 'rocknroll']
  >>> sorted(animal.all_animals.keys())
  ['dragon', 'sperm whale', 'whale']

GlobalGrokker
-------------

Sometimes you want to let a grok action happen for each module. The
grok action could for instance read the globals of a module, or even
static files associated with the module by name. Let's create a module
with some global value::

  >>> class g(FakeModule):
  ...   amount = 50
  >>> g = fake_import(g)
 
Now let's create a ``GlobalGrokker`` that reads ``amount`` and stores
it in the ``read_amount`` dictionary::

  >>> read_amount = {}
  >>> from martian import GlobalGrokker
  >>> class AmountGrokker(GlobalGrokker):
  ...   def grok(self, name, module):
  ...     read_amount[None] = module.amount
  ...     return True

Let's construct a ``ModuleGrokker`` with this ``GlobalGrokker`` registered::

  >>> grokker = ModuleGrokker()
  >>> grokker.register(AmountGrokker())

Now we grok and should pick up the right value::

  >>> grokker.grok('g', g)
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

Let's make a grokker for the old style class::

  >>> class MachineGrokker(ClassGrokker):
  ...   component_class = oldstyle.Machine
  ...   def grok(self, name, obj):
  ...     oldstyle.all_machines[name] = obj
  ...     return True

And another grokker for old style instances::

  >>> class MachineInstanceGrokker(InstanceGrokker):
  ...   component_class = oldstyle.Machine
  ...   def grok(self, name, obj):
  ...     oldstyle.all_machine_instances[name] = obj
  ...     return True

The multi grokker should succesfully grok the old-style ``Machine`` class
and instances of it::

  >>> multi = MultiGrokker()
  >>> multi.register(MachineGrokker())
  >>> multi.register(MachineInstanceGrokker())
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

Grokking a package
------------------

A package consists of several sub modules. When grokking a package,
all the files in the package will be grokked. Let's first create a simple
grokker for the ``Animal`` class defined by the package::

  >>> from martian.tests.testpackage import animal
  >>> all_animals = {}
  >>> class AnimalGrokker(ClassGrokker):
  ...   component_class = animal.Animal
  ...   def grok(self, name, obj, **kw):
  ...     all_animals[name] = obj
  ...     return True

The grokker will collect animals into the ``all_animals`` dictionary.

Let's register this grokker for a ModuleGrokker::

  >>> module_grokker = ModuleGrokker()
  >>> module_grokker.register(AnimalGrokker())

Now let's grok the whole ``testpackage`` for animals::

  >>> from martian import grok_dotted_name
  >>> grok_dotted_name('martian.tests.testpackage', grokker=module_grokker)
  
We should now get some animals::

  >>> sorted(all_animals.keys())
  ['Animal', 'Bear', 'Dragon', 'Lizard', 'Python', 'SpermWhale', 'Whale']

Preparation and finalization
----------------------------

Before grokking a module, it may be that we need to do some
preparation. This preparation can include setting up some parameters
to pass along to the grokking process, for instance. We can pass
a ``prepare`` function a the ModuleGrokker::

  >>> class Number(object):
  ...   def __init__(self, nr):
  ...     self.nr = nr
  >>> all_numbers = {}
  >>> class NumberGrokker(InstanceGrokker):
  ...  component_class = Number
  ...  def grok(self, name, obj, multiplier):
  ...    all_numbers[obj.nr] = obj.nr * multiplier
  ...    return True
  >>> def prepare(name, module, kw):
  ...   kw['multiplier'] = 3
  >>> module_grokker = ModuleGrokker(prepare=prepare)
  >>> module_grokker.register(NumberGrokker())
 
We have created a ``prepare`` function that does one thing: create a
``multiplier`` parameter that is passed along the grokking
process. The ``NumberGrokker`` makes use of this to prepare the
``all_numbers`` dictionary values.

Let's try this with a module::

  >>> class numbers(FakeModule):
  ...   one = Number(1)
  ...   two = Number(2)
  ...   four = Number(4)
  >>> numbers = fake_import(numbers)
  >>> module_grokker.grok('numbers', numbers)
  True
  >>> sorted(all_numbers.items())
  [(1, 3), (2, 6), (4, 12)]

You can also optionally register a finalization function, which will
be run at the end of a module grok::

  >>> def finalize(name, module, kw):
  ...     all_numbers['finalized'] = True
  >>> module_grokker = ModuleGrokker(prepare=prepare, finalize=finalize)
  >>> module_grokker.register(NumberGrokker())
  >>> all_numbers = {}
  >>> module_grokker.grok('numbers', numbers)
  True
  >>> 'finalized' in all_numbers
  True

Sanity checking
---------------

Grokkers must return ``True`` if grokking succeeded, or ``False`` if
it didn't. If they return something else (typically ``None`` as the
programmer forgot to), the system will raise an error::

  >>> class BrokenGrokker(InstanceGrokker):
  ...  component_class = Number
  ...  def grok(self, name, obj):
  ...    pass

  >>> module_grokker = ModuleGrokker()
  >>> module_grokker.register(BrokenGrokker())
  >>> module_grokker.grok('numbers', numbers) 
  Traceback (most recent call last):
    ...
  GrokError: <BrokenGrokker object at ...> returns None instead of 
  True or False.

Let's also try this with a GlobalGrokker::

  >>> class MyGrokker(GlobalGrokker):
  ...   def grok(self, name, module):
  ...     return "Foo"
  >>> module_grokker = ModuleGrokker()
  >>> module_grokker.register(MyGrokker())
  >>> module_grokker.grok('numbers', numbers)
  Traceback (most recent call last):
    ...
  GrokError: <MyGrokker object at ...> returns 'Foo' instead of True or False.
