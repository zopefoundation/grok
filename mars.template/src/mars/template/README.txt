=============
Mars Template
=============

Martian is a library that allows the embedding of configuration
information in Python code. Martian can then grok the system and
do the appropriate configuration registrations.

z3c packages bring significant clarity and a pattern for forms, view and
templates.

This package uses martian to configure z3c.template based templates.

Example Code
------------

::

    class View(grok.View):

        def render(self):
            template = zope.component.getMultiAdapter(
                (self, self.request), IPageTemplate)
            return template(self)

    class ViewTemplate(mars.template.TemplateFactory):
        grok.template('templates/macro.pt')
        grok.context(View)
        mars.template.macro('mymacro')

Directives
----------

Please see ``directive.txt``.

Tests
-----

See test directory.

