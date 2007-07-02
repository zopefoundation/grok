from martian.directive import (InterfaceOrClassDirective,
                            ClassDirectiveContext)

layout = InterfaceOrClassDirective('megrok.template.layout',
                           ClassDirectiveContext())
macro = InterfaceOrClassDirective('megrok.template.macro',
                           ClassDirectiveContext())
content_type = InterfaceOrClassDirective('megrok.template.content_type',
                           ClassDirectiveContext())
