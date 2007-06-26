from martian.directive import SingleTextDirective, ClassOrModuleDirectiveContext

qux = SingleTextDirective('grok.qux', ClassOrModuleDirectiveContext())

qux('hello world')
