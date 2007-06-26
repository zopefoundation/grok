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

Martian provides a framework that allows configuration to be expressed
in declarative Python code. These declarations can often be decuded
from the structure of the code itself. The idea is to make these
declarations so minimal and easy to read that even extensive
configuration does not overly burden the programmers working with the
code. Configuration actions are executed during a separate phase
("grok time"), not at import time, which makes it easier to reason
about and easier to test.

The ``martian`` package is a spin-off from the `Grok project`_, in the
context of which this codebase was first developed. While Grok uses
it, the code is completely independent of Grok.

For more information about using Martian, see:

  src/martian/README.txt
  src/martian/directive.txt
  src/martian/scan.txt

.. _`Grok project`: http://grok.zope.org
