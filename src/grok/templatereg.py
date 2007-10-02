from martian.error import GrokError

import os
import zope.component
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

            #import pdb
            #pdb.set_trace()

            template_name, extension = os.path.splitext(template_file)
            extension = extension[1:] # Get rid of the leading dot.
            template_factory = zope.component.queryUtility(
                grok.interfaces.ITemplateFactory,
                name=extension)
                
            if template_factory is None:
                # Warning when importing files. This should be
                # allowed because people may be using editors that generate
                # '.bak' files and such.
                warnings.warn("File '%s' has an unrecognized extension in "
                              "directory '%s'" %
                              (template_file, template_dir), UserWarning, 2)
                continue

            inline_template = self.get(template_name)
            if inline_template:
                raise GrokError("Conflicting templates found for name '%s' "
                                "in module %r, either inline and in template "
                                "directory '%s', or two templates with the "
                                "same name and different extensions."
                                % (template_name, module_info.getModule(),
                                   template_dir), inline_template)

            template = template_factory(template_file, template_dir)
            template_path = os.path.join(template_dir, template_file)
            template._annotateGrokInfo(template_name, template_path)

            self.register(template_name, template)

    def listUnassociated(self):
        for name, entry in self._reg.iteritems():
            if not entry['associated']:
                yield name


class PageTemplateFileFactory(grok.GlobalUtility):
    
    grok.implements(grok.interfaces.ITemplateFactory)
    grok.name('pt')
    
    
    def __call__(self, filename, _prefix=None):
        return grok.components.PageTemplateFile(filename, _prefix)
    