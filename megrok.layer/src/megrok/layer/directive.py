from grok.directive import (InterfaceOrClassDirective,
                            ClassOrModuleDirectiveContext)

layer = InterfaceOrClassDirective('megrok.layer.layer',
                           ClassOrModuleDirectiveContext())
