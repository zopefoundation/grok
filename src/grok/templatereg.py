from martian.error import GrokError
from martian import util

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

    def checkUnassociated(self, module_info):
        unassociated = list(self.listUnassociated())
        if unassociated:
            raise GrokError("Found the following unassociated template(s) when "
                            "grokking %r: %s.  Define view classes inheriting "
                            "from grok.View to enable the template(s)."
                            % (module_info.dotted_name,
                               ', '.join(unassociated)), module_info)

    def checkTemplates(self, module_info, factory, factory_name):
        template_name = util.class_annotation(factory, 'grok.template',
                                              factory_name)
            
        if factory_name != template_name:
            # grok.template is being used
    
            if self.get(factory_name):
                raise GrokError("Multiple possible templates for view %r. It "
                                "uses grok.template('%s'), but there is also "
                                "a template called '%s'."
                                % (factory, template_name, factory_name),
                                factory)
        template = self.get(template_name)
        if template:
            if (getattr(factory, 'render', None) and not
                util.check_subclass(factory, grok.components.GrokForm)):
                # we do not accept render and template both for a view
                # (unless it's a form, they happen to have render.
                raise GrokError(
                    "Multiple possible ways to render view %r. "
                    "It has both a 'render' method as well as "
                    "an associated template." % factory, factory)
            self.markAssociated(template_name)
            factory.template = template
        else:
            if not getattr(factory, 'render', None):
                # we do not accept a view without any way to render it
                raise GrokError("View %r has no associated template or "
                                "'render' method." % factory, factory)
