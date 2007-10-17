import os
import codecs
import sys
import urllib

import docutils.core
from docutils.writers.html4css1 import Writer

from zope.app.renderer.rest import ZopeTranslator
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

# registers code-block directive using pygments.
import pygments_code_block_directive

class ReStructuredTextToHTMLRenderer:
    """Convert from Restructured Text to HTML."""

    def __init__(self,content):
        self.content = content 

    def render(self):
        settings_overrides = {
            'halt_level': 6,
            'input_encoding': 'utf8',
            'output_encoding': 'utf8',
            'initial_header_level': 2,
            # don't try to include the stylesheet (docutils gets hiccups)
            'stylesheet_path': '',
        }

        writer = Writer()
        writer.translator_class = ZopeTranslator
        html = docutils.core.publish_string(
                        self.content,
                        writer=writer,
                        settings_overrides=settings_overrides,)
        html = codecs.decode(html, 'utf_8')
        return html

class RestFile(object):
    
    source = ''
    target = ''
    url = ''
    title = ''
    active = True

    def __init__(self, url, source, target):
        self.url = url
        self.target = target
        if os.path.isfile(target) and os.path.isfile(source):
            if os.path.getmtime(source) < os.path.getmtime(target):
                self.active = False
        if os.path.isfile(source):
            self.source = codecs.open(source,"r",'utf8').read()
        elif source.startswith("http"):
            print "Downloading %s" % source
            try:
                response = urllib.urlopen(source)
                self.source = response.read()
            except IOError, e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'):
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code:', e.code
                self.source = u''
        else:
            self.source = source
        srctxt = self.source.split('\n')
        title = ''
        count = 0
        while title == '':
            title = srctxt[count]
            count += 1
            if title.startswith("=====") or title.startswith(".."):
                title = srctxt[count]
        self.title = title

    def set_rest_content(self):
        renderer = ReStructuredTextToHTMLRenderer(self.source)
        self.content = renderer.render().strip()

    def create_html(self, page, settings):
        if not self.active:
            pass
        print 'Processing ', self.url
        self.set_rest_content()

        settings["context"] = Context(self.url, self.title, self.content)
        content = page.pt_render(namespace=settings)
        #fp = open(self.target, 'w')
        targetdir = os.path.dirname(self.target)
        if not os.path.isdir(targetdir):
            print 'Creating dir: ', targetdir
            os.mkdir(targetdir)
        fp = codecs.open(self.target,"w",'utf8')
        fp.write(content)
        fp.close()

class Context:
    """Set up the context for rendering the rest as html through zpt"""

    def __init__(self, url, title=u'', content=u''):
        self.url = url
        self.title = title
        self.content = content

    @property
    def menu(self):
        for item in Menu:
            if item.get('href') == self.url:
                item['klass'] = u'selected'
            else:
                item['klass'] = u''
            # just for tutorial files
            if len(self.url.split('/')) > 2:
                if item.get('href').split('/')[:-1] == self.url.split('/')[:-1]:
                    item['klass'] = u'selected'
            if not item.get('description', None):
                item['description'] = item['title']
        return Menu

def create_html(rest_files, template):
    settings = {}
    settings["here"] = { "layout": template }
    page = PageTemplate()
    page.write("""<metal:block use-macro="here/layout/macros/pagelayout" />""")

    for restfile in rest_files:
        restfile.create_html(page, settings)

# Menu should later be generated if site becomes more complex
Menu = [
        {'href':'/index.html','title':u'Home','klass':''},
        {'href':'/about.html','title':u'About','klass':''},
        {'href':'/tutorial.html','title':u'Tutorial','klass':''},
        {'href':'/minitutorials/index.html','title':u'How Tos','klass':''},
        ]

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not len(argv) == 1:
        print "Usage: grok2html OUTDIR"
        sys.exit(1)

    source_dir = os.path.dirname(__file__)
    www_dir = os.path.abspath(argv[0])

    if not os.path.isdir(www_dir):
        print "OUTDIR '%s' does not exist." % (www_dir,)
        sys.exit(1)
    
    os.chdir(source_dir)

    rest_files = []
    rest_files.append(RestFile('index', 
                              os.path.join(source_dir, 'index.txt'),
                              os.path.join(www_dir, 'index.html')))
    rest_files.append(RestFile('about', 
                              os.path.join(source_dir, 'about.txt'),
                              os.path.join(www_dir, 'about.html')))
    rest_files.append(RestFile('tutorial', 
                              os.path.join(source_dir, 'tutorial.txt'),
                              os.path.join(www_dir, 'tutorial.html')))
    rest_files.append(RestFile('mini-index', 
                              os.path.join(source_dir, 'minitutorials', 'index.txt'),
                              os.path.join(www_dir, 'minitutorials', 'index.html')))
    rest_files.append(RestFile('searching', 
                              os.path.join(source_dir, 'minitutorials', 'searching.txt'),
                              os.path.join(www_dir, 'minitutorials', 'searching.html')))
    rest_files.append(RestFile('macros', 
                              os.path.join(source_dir, 'minitutorials', 'macros.txt'),
                              os.path.join(www_dir, 'minitutorials', 'macros.html')))
    rest_files.append(RestFile('xmlrpc', 
                              os.path.join(source_dir, 'minitutorials', 'xmlrpc.txt'),
                              os.path.join(www_dir, 'minitutorials', 'xmlrpc.html')))
    rest_files.append(RestFile('permissions', 
                              os.path.join(source_dir, 'minitutorials', 'permissions.txt'),
                              os.path.join(www_dir, 'minitutorials', 'permissions.html')))
    rest_files.append(RestFile('transient-objects', 
                              os.path.join(source_dir, 'minitutorials', 'transient-objects.txt'),
                              os.path.join(www_dir, 'minitutorials', 'transient-objects.html')))
    rest_files.append(RestFile('zc.buildout', 
                  'http://svn.zope.org/*checkout*/zc.buildout/trunk/doc/tutorial.txt',
                  os.path.join(www_dir, 'minitutorials', 'buildout.html')))
    template = PageTemplateFile(os.path.join(source_dir, 'template.pt'))
    create_html(rest_files, template)

if __name__ == '__main__':
    main()
