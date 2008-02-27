"""
Schema-driven development with grok
"""
import grok

grok.directory('contact')

class Contact(grok.SchemaModel):
    """
    This works now:

      >>> c = Contact(name=u'Martijn', city=u'Rotterdam')
      >>> c.name
      u'Martijn'

    Also w/o kw:

      >>> c = Contact(u'Martijn', u'Rotterdam')
      >>> c.name
      u'Martijn'

    """
    class fields:
        name = schema.TextLine()
        city = schema.TextLine()


class Edit(grok.EditForm):
    pass
    # this will automatically render an edit form, and use an
    # 'edit.html' template if available

class Index(grok.DisplayForm):
    pass
    # this will automatically render an display form, and use an
    # 'index.html' template if available

class Add(grok.AddForm):
    grok.context(Contact)  # this is actually the default
    grok.container(IContainer)  # this is actually the default

class FancyEdit(grok.EditForm):
    """ use cases:

    * (actions with permissions)

    *

    """

    @grok.action("Save")
    def save(self, **data):
        """
        this overrides any actions defined on the base class
        """
        self.applyChanges(data)
