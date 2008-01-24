=========================
Automatic Form Generation
=========================

:Author: Dirceu Pereira Tiegs

Introduction
------------

Grok supports automatic form generation by working with zope.interface, zope.schema and zope.formlib. This how-to will show you how to create an application that uses this feature and also how to use some more advanced widgets than the formlib defaults.

Schema and Fields
-----------------

Fields are components that define a model's attributes, and schemas are collections of fields. For example:

+-------------------+
| Person            |
+-------------------+
| name: String      |
+-------------------+
| birth: Date       |
+-------------------+
| description: Text |
+-------------------+

The model above can be translated into Grok code like this:

.. code-block:: python

    from zope import interface, schema
    class IPerson(interface.Interface):
        name = schema.TextLine(title="Name")
        birth = schema.Date(title="Birth")
        description = schema.Text(title="Description")

Defining an interface with schema fields allows automatic form generation and validation. To do this, grok.AddForm, grok.EditForm and grok.DisplayForm are used. These components are called forms; forms are web components that use widgets to display and input data. Typically a template renders the widgets by calling attributes or methods of the displayed object.

Widgets are components that display field values and, in the case of writable fields, allow the user to edit those values. Widgets:

- Display current field values, either in a read-only format, or in a format that lets the user change 
  the field value.

- Update their corresponding field values based on values provided by users.

- Manage the relationships between their representation of a field value and the object's field value.
  For example, a widget responsible for editing a number will likely represent that number internally as
  a string. For this reason, widgets must be able to convert between the two value formats. In the case
  of the number-editing widget, string values typed by the user need to be converted to numbers such as
  int or float.

- Support the ability to assign a missing value to a field. For example, a widget may present a ``None`` 
  option for selection that, when selected, indicates that the object should be updated with the field's 
  ``missing`` value.


The forms have default templates that are used if no other template is provided. 

grok.AddForm and grok.EditForm use the default template [grok_egg]/templates/default_edit_form.pt. 

grok.DisplayForm uses [grok_egg]/templates/default_display_form.pt.

Input Validation - Constraints and Invariants
---------------------------------------------

A constraint is constraint (:-)) that is bound to a specific field:

.. code-block:: python

    import grok
    from zope import interface, schema
    import re

    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=?^_`{}|~]+"
                      r"@(([0-9a-z]([0-9a-z-]*[0-9a-z])?\.)+[a-z]{2,6}|([0-9]{1,3}"
                      r"\.){3}[0-9]{1,3})$", re.IGNORECASE)
    check_email = expr.match

    class IMyUser(interface.Interface):
        email = schema.TextLine(title="Email", constraint=check_email)

    class MyUser(grok.Model)
        interface.implements(IMyUser)

        def __init__(self, email):
            super(MyUser, self).__init__()
            self.email = email

An invariant is a constraint that involves more than one field:

.. code-block:: python

    import grok
    from zope import interface, schema
    from datetime import date

    class IMyEvent(interface.Interface):
        title = schema.TextLine(title="Title")
        begin = schema.Date(title="Begin date")
        end = schema.Date(title="End date")

    class MyEvent(grok.Model)
        interface.implements(IMyEvent)

        def __init__(self, title, begin, end):
            super(MyEvent, self).__init__()
            self.title = title
            self.begin = begin
            self.end = end

        @interface.invariant
        def beginBeforeEnd(event):
            if event.begin > event.end:
                raise interface.Invalid("Begin date must be before end date")

Example 1 - Birthday Reminder
-----------------------------

Grok want to remember his friends's birthday, so he created a simple application to do that.

ME GROK SMASH CALENDAR!

We want to use a custom widget to select dates, so you need to add 'z3c.widget' to setup.py of your package:

.. code-block:: python

    install_requires=['setuptools',
                      'grok',
                      'z3c.widget',
                      # Add extra requirements here
                      ],

And run ./bin/buildout. This will install z3c.widget and make it available to your project.

app.py is pretty simple:

.. code-block:: python

    import grok

    class Friends(grok.Application, grok.Container):
        pass

    class Index(grok.View):
        pass

friend.py contains our content component and it's forms:

.. code-block:: python

    import grok
    from zope import interface, schema
    from app import Friends

    from z3c.widget.dropdowndatewidget.widget import DropDownDateWidget

    class IFriend(interface.Interface):
        name = schema.TextLine(title=u"Name")
        birth_date = schema.Date(title=u"Birth Date")
        description = schema.Text(title=u"Description")

    class Friend(grok.Model):
        interface.implements(IFriend)
    
        def __init__(self, name, birth_date, description):
            super(Friend, self).__init__()
            self.name = name
            self.birth_date = birth_date
            self.description = description

    class AddFriend(grok.AddForm):
        grok.context(Friends)
        form_fields = grok.AutoFields(Friend)

        # Here is the trick. You set the 'custom_widget' attribute with the custom Widget's class
        form_fields['birth_date'].custom_widget = DropDownDateWidget

        @grok.action('Add event')
        def add(self, **data):
            obj = Friend(**data)
            name = data['name'].lower().replace(' ', '_')
            self.context[name] = obj

    class Edit(grok.EditForm):
        form_fields = grok.AutoFields(Friend)
        form_fields['birth_date'].custom_widget = DropDownDateWidget

    class Index(grok.DisplayForm):
        pass


Example 2 - Wiki
----------------

Grok wants to impress beautiful cavewomen with a cool Web 2.0 application, so he built a Wiki with a JavaScript enabled text editor. 

ME GROK WANTS COLLABORATE AND RICH TEXT EDITOR!

You need to add 'zc.resourcelibrary' and 'z3c.widget' to setup.py of your package and run ./bin/buildout to install the new components:

setup.py

.. code-block:: python

    install_requires=['setuptools',
                      'grok',
                      'zc.resourcelibrary',
                      'z3c.widget',
                      # Add extra requirements here
                      ],

app.py won't contain any application logic, only the application and the default view called "index".

.. code-block:: python

    import grok

    class Wiki(grok.Application, grok.Container):
        pass

    class Index(grok.View):
        pass

wikipage.py is almost identical to friend.py in our first example:

.. code-block:: python

    import grok
    from zope import interface, schema
    from app import Wiki

    from z3c.widget.tiny.widget import TinyWidget

    class IWikiPage(interface.Interface):
        title = schema.TextLine(title=u"Title")
        contents = schema.Text(title=u"Contents")

    class WikiPage(grok.Model):
        interface.implements(IWikiPage)
    
        def __init__(self, title, contents):
            super(WikiPage, self).__init__()
            self.title = title
            self.contents = contents

    class AddWikiPage(grok.AddForm):
        grok.context(Wiki)
        form_fields = grok.AutoFields(WikiPage)
        form_fields['contents'].custom_widget = TinyWidget

        @grok.action('Add event')
        def add(self, **data):
            obj = WikiPage(**data)
            name = data['title'].lower().replace(' ', '_')
            self.context[name] = obj

    class Edit(grok.EditForm):
        form_fields = grok.AutoFields(WikiPage)
        form_fields['contents'].custom_widget = TinyWidget

    class Index(grok.DisplayForm):
        pass

Here is the trick: to use TinyWidget you must load it's configuration. TinyWidget uses zc.resourcelibrary to load the JavaScript editor, and zc.resourcelibrary have some dependencies (on zope.app.component and zope.app.pagetemplate). Your package's configure.zcml must be like this:

.. code-block:: html

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:grok="http://namespaces.zope.org/grok">
      <include package="zope.app.component" file="meta.zcml" />
      <include package="zope.app.pagetemplate" file="meta.zcml" />
      <include package="zc.resourcelibrary" file="meta.zcml" />
      <include package="zc.resourcelibrary" />
      <include package="z3c.widget.tiny" />
      <include package="grok" />
      <grok:grok package="." />
    </configure>

And we must add a directive to the AddForm template to load the TinyMCE editor. First, copy the default template:

.. code-block:: sh

    $ mkdir wikipage_templates 
    $ cp [grok_egg]/grok/templates/default_edit_form.pt wikipage_templates/addwikipage.pt

Then add this directive to the <head> tag of wikipage_templates/addwikipage.pt

.. code-block:: html

  <head>
    <tal:block replace="resource_library:tiny_mce" />
  </head>

And that's it! Now AddWikiPage uses TinyMCE to edit the "contents" field.

Learning More
-------------

Many topics not were covered here. You can learn more reading the source code of Zope 3 components such as zope.schema and zope.formlib. Zope is a great platform and have a pretty good automated testing culture, so you can evend read / run doctests like these:

- http://svn.zope.org/zope.schema/trunk/src/zope/schema/README.txt?rev=80304&view=auto
- http://svn.zope.org/zope.schema/trunk/src/zope/schema/fields.txt?rev=75170&view=auto
- http://svn.zope.org/zope.schema/trunk/src/zope/schema/validation.txt?rev=79215&view=auto
- http://svn.zope.org/zope.formlib/trunk/src/zope/formlib/form.txt?rev=81649&view=markup
- http://svn.zope.org/zope.formlib/trunk/src/zope/formlib/errors.txt?rev=75131&view=markup

Web Component Development with Zope 3 is a great book written by Philipp von Weitershausen (wich is a Grok core developer). While the book doesn't cover Grok directly, it covers all the underlying technology that Grok uses:

- http://worldcookery.com/
