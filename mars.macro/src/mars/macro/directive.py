from martian.directive import (InterfaceOrClassDirective,
                               SingleTextDirective,
                               ClassDirectiveContext)

macro = SingleTextDirective('mars.macro.macro',
                           ClassDirectiveContext())
view = InterfaceOrClassDirective('mars.macro.view',
                           ClassDirectiveContext())
content_type = SingleTextDirective('mars.macro.content_type',
                           ClassDirectiveContext())

