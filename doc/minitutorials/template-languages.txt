==================================
Plugging in new template languages
==================================

:Author: Lennart Regebro

Introduction
------------

Grok, like the Zope 3 framework on which it is built, uses Zope Page
Templates as its default templating language.  While you can, of
course, use whatever templating language you want in Grok by calling
it manually, you can also “plug in” a template language such that both
inline templates and templates stored in files are automatically
linked with your Views — just like inline ``grok.PageTemplates`` and
files with the ``.pt`` extension are by default.


Inline templates
----------------

“Inline” templates are templates that you create right in your Python
code — for example, by instantiating the default ``grok.PageTemplate``
class with a literal string value as its argument.  Such templates are
automatically associated with nearby ``View`` classes: if you create a
View named ``Mammoth`` and next to it instantiate a template named
``mammoth``, then Grok will use them together.

To enable such automatic association for a new templating language, you need
to write a subclass of ``grok.components.GrokTemplate``. You will need to
override three methods. The ``setFromFilename`` and ``setFromString`` methods
should each load the template from disk or a given string, depending on
method. Your ``render`` method should run the template with the dictionary of
values returned by ``self.getNamespace()`` and return the resulting string.

Here is an example of a minimal page template integration:

.. code-block:: python

class MyPageTemplate(grok.components.GrokTemplate):

    def setFromString(self, string):
        self._template = MyTemplate(string)

    def setFromFilename(self, filename, _prefix=None):
        file = open(os.path.join(_prefix, filename))
        self._template = MyTemplate(file.read())

    def render(self, view):
        return self._template.render(\**self.getNamespace(view))

With this class finished you can create an inline template, like this:

.. code-block:: python

    class AView(grok.View):
        pass

    aview = MyPageTemplate('<html><body>Some text</body></html>')

And also you can create a filebase template, inline:

.. code-block:: python

    class AView(grok.View):
        pass

    aview = MyTemplateFile('lasceuax.html')


Templates in the _templates directory
-------------------------------------

The most common use case, however, is to place templates for a file
``foo.py`` in the corresponding ``foo_templates`` directory.  Grok, of
course, already recognizes that files with a ``.pt`` extension each
contain a Zope Page Template.  To tell Grok about a new file
extension, simply register a global utility that generates a
``MyPageTemplate`` when passed a filename.  That utility needs to
implement the ``ITemplateFileFactory`` interface.

.. code-block:: python

class MyPageTemplateFactory(grok.GlobalUtility):

    grok.implements(grok.interfaces.ITemplateFileFactory)
    grok.name('mtl')

    def __call__(self, filename, _prefix=None):
        return MyPageTemplate(filename=filename, _prefix=_prefix)

When your module gets grokked, Grok will discover the
``MyPageTemplateFactory`` class, register it as a global utility for
templates with the ``.mtl`` extension, and you can start creating
``.mtl`` files in the template directory for your class.

That's all you need!  Have fun!
