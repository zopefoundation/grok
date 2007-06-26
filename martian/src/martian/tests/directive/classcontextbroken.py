from martian.directive import SingleTextDirective, ClassDirectiveContext

bar = SingleTextDirective('grok.bar', ClassDirectiveContext())

bar('hello world') # this won't work as not class context
