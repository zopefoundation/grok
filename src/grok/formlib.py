import types
from zope import interface
from zope.interface.interfaces import IInterface
from zope.formlib import form
from zope.schema.interfaces import IField

class action(form.action):
    """We override the action decorator we pass in our custom Action.
    """
    def __call__(self, success):
        action = Action(self.label, success=success, **self.options)
        self.actions.append(action)
        return action

class Action(form.Action):
    def success(self, data):
        if self.success_handler is not None:
            return self.success_handler(self.form, **data)

def Fields(*args, **kw):
    fields = []
    for key, value in kw.items():
        if IField.providedBy(value):
            value.__name__ = key
            fields.append(value)
            del kw[key]
    fields.sort(key=lambda field: field.order)
    return form.Fields(*(args + tuple(fields)), **kw)

def get_context_schema_fields(context):
    """Get the schema fields for a context object.
    """
    fields = []
    fields_class = getattr(context, 'fields', None)
    # bail out if there is no fields attribute at all
    if fields_class is None:
        return fields
    # bail out if there's a fields attribute but it isn't an old-style class
    if type(fields_class) != types.ClassType:
        return fields
    # get the fields from the class
    for name in dir(fields_class):
        field = getattr(fields_class, name)
        if IField.providedBy(field):
            if not getattr(field, '__name__', None):
                field.__name__ = name
            fields.append(field)
    fields.sort(key=lambda field: field.order)
    return fields

def get_auto_fields(context):
    """Get the form fields for context.
    """
    # for an interface context, we generate them from that interface
    if IInterface.providedBy(context):
        return form.Fields(context)
    # if we have a non-interface context,
    # we're autogenerating them from any model-specific
    # fields along with any schemas defined by the context
    fields = form.Fields(*get_context_schema_fields(context))
    fields += form.Fields(*most_specialized_interfaces(context))
    # we pull in this field by default, but we don't want it in our form
    fields = fields.omit('__name__')
    return fields

AutoFields = get_auto_fields

def most_specialized_interfaces(context):
    """Get interfaces for an object without any duplicates.

    Interfaces in a declaration for an object may already have been seen
    because it is also inherited by another interface. Don't return the
    interface twice, as that would result in duplicate names when creating
    the form.
    """
    declaration = interface.implementedBy(context)
    seen = []
    for iface in declaration.flattened():
        if interface_seen(seen, iface):
            continue
        seen.append(iface)
    return seen

def interface_seen(seen, iface):
    """Return True if interface already is seen.
    """
    for seen_iface in seen:
        if seen_iface.extends(iface):
            return True
    return False
