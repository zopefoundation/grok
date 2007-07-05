from mars.view.components import TemplateViewBase

class ContentProvider(TemplateViewBase):

    def __init__(self, context, request, view):
        self.__parent__ = self.view = view
        self.context = context
        self.request = request
