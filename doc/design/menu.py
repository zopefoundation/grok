"""megrok.menu

A simple but extensible menu system for Zope 3.

What is a menu?

    For web applications there are two competing design patterns that can be
    handled under the term 'menu': classic GUI menus and web site navigation.

    The essential difference in those two is the 'status' or 'context' of the
    menu. In classic GUI applications, a menu is (more or less) stateless,
    independent of the view to the application that is currently being used.

    In classic web sites, the navigation gives a navigatable overview of the
    site's hierarchy using an 'active' flag to indicate the user's position in
    the site.

    In web applications those two concepts start to mix.

    The basic implementation of the menu system takes care of the classic
    listing of options a user has in a specific context.

    An extension mechanism is used to provide status-annotation to menu items
    to show where a user currently is.

Design goals:

    -   Simple, central, menu definition without ZCML

    -   Allow submenus.

    -   Make status determination pluggable to allow for application-specific
        complex scenarios without tainting the menu system.

Menu rendering process:

    -   create set of choices (apply filters in context, permissions, condition)

    -   apply (status) annotations

Determining whether an item is active:

    a) Model based

    - find out which object belongs to the menu item

    - Is this object the same as the context of the menu?

    b) View based

    - find out which view belongs to the menu item

    - Is it the currently published view?

    Generalisation: 

Zope/Grok stuff:

    -   Menus are utilities

Questions:

    -   How to integrate with skin layers?  

    -   Aren't menus just browser views? (context, request)

    -   Two variations: allow menu items to render their HTML, or not? 

        Allow HTML:

            - provides ability to implement various menu item types

            - codes in presentation

        Don't allow HTML:

            - more flexible to customize?

        -> use views on menu items!
"""

import grok
from megrok import menu

class AddressBook(grok.Model):
    pass

class Contact(grok.Model):
    pass

class EditContact(grok.EditForm):
    grok.context(Contact)
    grok.annotation("title", _(u"Edit XY"))


layout = grok.PageTemplate("""\
<html>
<body>

    <!-- Most simple: Render the whole menu -->
    <div tal:replace="structure menu/main/@@links"/>

    <!-- Variation 1: Render whole menu as drop down list -->
    <div tal:replace="structure menu/main/@@dropdown"/>

    <!-- Variation 2: Render menu manually, get each item as link
    <ul>
        <li tal:repeat="item menu/main">
            <a tal:replace="structure item/@@link">
        </li>
    </ul>

    <!-- Variation 3: Render menu and items manually 
    <ul tal:repeat="item menu/main"><a tal:attributes="href item/action" tal:content="item/title"></ul>
    </ul>

    <!-- Variation 4: Render option elements automatically -->
    <select>
        <option tal:repeat="item menu:main" tal:replace="item/@@option">
    </select>

    <!-- Bind the menu to a different object explicitly -->
    <div tal:replace="structure python:menu['main'].bind(object1, request)"/>
    '
    <!-- Alternative: use a grok variable in the templates: -->
    <div tal:replace="structure grok/menu/main/context:asdf/"/>



    <grok:menu 
</body>
</html>""")

class IMenuItem(Interface):

    action
    title
    submenu


main = menu.Menu(
    menu.View(EditContact),         # Link to a view. Necessary information: context, name
                                    # Link to a generic action/URL
    menu.Action(_("External action"), "string:http://${context/"),
    menu.SubMenu(
        menu.Item(


############ Implementation sketches

class ViewMenuItem(object):

    def __init__(self, view):
        # View must be a view
        

class Action(object):
    
    def __init__(self, title, target):
        self.title = title
        self.target = target    # TALES expression

    def 


class BaseMenuItem(object):

    def __init__(self, condition):
        self.condition = condition

    def checkCondition(context, request):
        # - does this item apply in the given context?
        # - does the user have the necessary permissions
        # - does the user supplied condition evalute to true? 
    

class Menu(object):

    def __init__(self, menu_items):
        # XXX assert: All items must be menu items
        self.menu_items = menu_items

    def __call__(self, context, request):
        relevant_items = []

        for item in self.menu_items:
            if not item.checkCondition(context, request):
                continue

            relevant_item.append(item)


