
import grokcore.component
import grok.events
import zope.event

from zope.generations.interfaces import IInstallableSchemaManager
from zope.generations.utility import getRootFolder


class GrokDatabaseCreated(grokcore.component.GlobalUtility):
    # The name starts with a null byte so that then they are sorted and
    # executed by zope.generation it ends up to be first.
    grokcore.component.name('\x00grok database created')
    grokcore.component.implements(IInstallableSchemaManager)

    minimum_generation = generation = 1

    def install(self, context):
        root = getRootFolder(context)
        zope.event.notify(grok.events.DatabaseCreatedEvent(root))

    def evolve(self, context, generation):
        pass
