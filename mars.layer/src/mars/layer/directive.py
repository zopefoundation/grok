from grok.directive import (InterfaceOrClassDirective,
                            ClassOrModuleDirectiveContext)

layer = InterfaceOrClassDirective('mars.layer.layer',
                           ClassOrModuleDirectiveContext())
