=========
Mars View
=========

Martian is a library that allows the embedding of configuration
information in Python code. Martian can then grok the system and
do the appropriate configuration registrations.

z3c packages bring significant clarity and a pattern for forms, view and
templates.

This package uses martian to configure views. The views here defined are
TemplateView and LayoutView, both use adapter lookup to locate the template to
be used (but can class attributes `template` for TemplateView and LayoutView and `layout` for
LayoutView will be used before adapter lookup).

TemplateView provides only a `render` method which returns the rendered
template.

LayoutView has a `__call__` method that returns the rendered layout template in
addition to a `render` method inherited from TemplateView which returns the
rendered template.

Example Code
------------

The following registers a view for Context named view. It has a
`render` method that renders the template defined by ViewTemplate::

 class Context(grok.Model):
     pass

 class View(mars.view.TemplateView):
     pass

 class ViewTemplate(mars.template.TemplateFactory):
     grok.template('templates/template.pt')
     grok.context(View)

The following snippet registers a view for Context named view. It has a
`__call__` method that renders the template defined by ViewLayout in addition to a
`render` method that renders the template defined by ViewTemplate::

 class Context(grok.Model):
     pass

 class View(mars.view.LayoutView):
     pass

 class ViewLayout(mars.template.LayoutFactory):
     grok.template('templates/template.pt')
     grok.context(View)

 class ViewSnippet(mars.template.TemplateFactory):
     grok.template('templates/snippet.pt')
     grok.context(View)


Directives
----------

Please see ``directive.txt``.

Tests
-----

See test directory.


