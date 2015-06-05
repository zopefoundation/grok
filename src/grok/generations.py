
import grokcore.component
import grok.events
import zope.event

from zope.generations.interfaces import IInstallableSchemaManager


class GrokDatabase(grokcore.component.GlobalUtility):
    grokcore.component.name('grok.database')
    grokcore.component.implements(IInstallableSchemaManager)

    minimum_generation = generation = 1

    def install(self, context):
        zope.event.notify(grok.events.DatabaseCreatedEvent(context))

    def evolve(self, context, generation):
        pass
