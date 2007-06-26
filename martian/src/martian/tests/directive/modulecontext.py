from martian.directive import SingleTextDirective, ModuleDirectiveContext

foo = SingleTextDirective('grok.foo', ModuleDirectiveContext())

foo('hello world')
