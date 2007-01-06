import os

from zope import interface, component
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import grok
from grok import util
from grok.error import GrokError


class TemplateRegistry(object):

    def __init__(self):
        self._reg = {}

    def register(self, name, template):
        self._reg[name] = dict(template=template, associated=False)

    def markAssociated(self, name):
        self._reg[name]['associated'] = True

    def get(self, name):
        entry = self._reg.get(name)
        if entry is None:
            return None
        return entry['template']

    def findFilesystem(self, module_info):
        template_dir_name = module_info.getAnnotation(
            'grok.templatedir',
            module_info.name + '_templates')

        template_dir = module_info.getResourcePath(template_dir_name)

        if not os.path.isdir(template_dir):
            return
        
        for template_file in os.listdir(template_dir):
            if template_file.startswith('.') or template_file.endswith('~'):
                continue

            if not template_file.endswith('.pt'):
                raise GrokError("Unrecognized file '%s' in template directory "
                                "'%s'." % (template_file, template_dir),
                                module_info.getModule())

            template_name = template_file[:-3] # cut off .pt
            template_path = os.path.join(template_dir, template_file)

            f = open(template_path, 'rb')
            contents = f.read()
            f.close()

            template = grok.PageTemplate(contents)
            template._annotateGrokInfo(template_name, template_path)

            inline_template = self.get(template_name)
            if inline_template:
                raise GrokError("Conflicting templates found for name '%s' "
                                "in module %r, both inline and in template "
                                "directory '%s'."
                                % (template_name, module_info.getModule(),
                                   template_dir), inline_template)
            self.register(template_name, template)

    def listUnassociated(self):
        for name, entry in self._reg.iteritems():
            if not entry['associated']:
                yield name, entry['template']

    def registerUnassociated(self, context, module_info):
        for name, unassociated in self.listUnassociated():
            util.check_context(unassociated, context)

            module_info_ = module_info
            class TemplateView(grok.View):
                template = unassociated
                module_info = module_info_

            self.markAssociated(name)

            TemplateView.__view_name__ = name
            component.provideAdapter(TemplateView,
                                     adapts=(context, IDefaultBrowserLayer),
                                     provides=interface.Interface,
                                     name=name)
