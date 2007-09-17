from martian.error import GrokError

import os
import grok
import warnings

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
            'grok.templatedir', module_info.name + '_templates')

        template_dir = module_info.getResourcePath(template_dir_name)

        if not os.path.isdir(template_dir):
            return
        
        for template_file in os.listdir(template_dir):
            if template_file.startswith('.') or template_file.endswith('~'):
                continue

            if not template_file.endswith('.pt'):
                # Warning when importing files. This should be
                # allowed because people may be using editors that generate
                # '.bak' files and such.
                warnings.warn("File '%s' has an unrecognized extension in "
                              "directory '%s'" %
                              (template_file, template_dir), UserWarning, 2)
                continue

            template_name = template_file[:-3] # cut off .pt
            template = grok.PageTemplateFile(template_file, template_dir)
            template_path = os.path.join(template_dir, template_file)
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
                yield name
