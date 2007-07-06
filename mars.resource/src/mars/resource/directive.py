from martian.directive import (InterfaceOrClassDirective,
                               SingleTextDirective,
                               ClassDirectiveContext)

file = SingleTextDirective('mars.resource.file',
                           ClassDirectiveContext())

image = SingleTextDirective('mars.resource.image',
                           ClassDirectiveContext())

directory = SingleTextDirective('mars.resource.directory',
                           ClassDirectiveContext())
