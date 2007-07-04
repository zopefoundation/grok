from martian.directive import (SingleTextDirective,
                               ClassDirectiveContext)

macro = SingleTextDirective('mars.template.macro',
                           ClassDirectiveContext())
content_type = SingleTextDirective('mars.template.content_type',
                           ClassDirectiveContext())

