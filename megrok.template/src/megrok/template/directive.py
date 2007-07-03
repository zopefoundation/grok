from martian.directive import (SingleTextDirective,
                               ClassDirectiveContext)

layout = SingleTextDirective('megrok.template.layout',
                           ClassDirectiveContext())
macro = SingleTextDirective('megrok.template.macro',
                           ClassDirectiveContext())
content_type = SingleTextDirective('megrok.template.content_type',
                           ClassDirectiveContext())
