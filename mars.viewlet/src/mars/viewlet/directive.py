from martian.directive import (InterfaceOrClassDirective,
                               ClassDirectiveContext)

manager = InterfaceOrClassDirective('mars.viewlet.manager',
                           ClassDirectiveContext())
view = InterfaceOrClassDirective('mars.viewlet.view',
                           ClassDirectiveContext())
