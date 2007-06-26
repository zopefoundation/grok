from martian.directive import OnceDirective, SingleValue, BaseTextDirective
from martian.directive import ModuleDirectiveContext

class MyDirective(BaseTextDirective, SingleValue, OnceDirective):
    pass

hoi = MyDirective('hoi', ModuleDirectiveContext())

hoi('once')
hoi('twice')
