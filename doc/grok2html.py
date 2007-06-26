import os

from zope.pagetemplate.pagetemplate import PageTemplate

import docutils.core
from docutils.writers.html4css1 import HTMLTranslator
from docutils.writers.html4css1 import Writer

class ZopeTranslator(HTMLTranslator):
    """
    The ZopeTranslator extends the base HTML processor for reST.  It
    augments reST by:

    - Outputs *only* the 'body' parts of the document tree, using the
    internal docutils structure.
    """

    def astext(self):
        """
        This is where we join the document parts that we want in
        the output.
        """
        # use the title, subtitle, author, date, etc., plus the content
        body = self.body_pre_docinfo + self.docinfo + self.body
        return u"".join(body)


class ReStructuredTextToHTMLRenderer:
    """convert from Restructured Text to HTML.

    """

    def __init__(self,content):
        self.content = content 

    def render(self):
        settings_overrides = {
            'halt_level': 6,
            'output_encoding': 'utf8',
            'initial_header_level': 2
        }
            # 'input_encoding': 'unicode',
            # 'output_encoding': 'unicode',
        writer = Writer()
        writer.translator_class = ZopeTranslator
        html = docutils.core.publish_string(
        self.content,
        writer=writer,settings_overrides=settings_overrides,)
        return html


Menu = [
        {'href':'index.html','title':u'Home','klass':''},
        {'href':'about.html','title':u'About','klass':''},
        {'href':'tutorial.html','title':u'Tutorial','klass':''},
        ]

class Context:
    """Set up the context for rendering the rest as html through zpt"""

    id = u''
    title = u''
    menu = []
    content = u''

    def __init__(self, id, title=u''):
        self.id = id
        self.title = title

    def restSource(self, source_file):
        fp = open(source_file)
        # try to locate a title for the document if not given
        if not self.title:
            self.title = fp.readline()
            if self.title.startswith("="):
                self.title = fp.readline()
        fp.close()
        #rest = codecs.open(source_file,"r",'utf8').read()
        rest = open(source_file).read()
        renderer = ReStructuredTextToHTMLRenderer(rest)
        return renderer.render().strip()
    
    def setRestContent(self, source_file):
        self.content = self.restSource(source_file)

    @property
    def menu(self):
        for item in Menu:
            if item.get('href').split('.')[0] == self.id:
                item['klass'] = u'selected'
            else:
                item['klass'] = u''
            if not item.get('description', None):
                item['description'] = item['title']
        return Menu

def handler_html(pageid, restpath):

# we could rename about_grok.txt to about.txt that we could use only 
# a pageid to identify the source document and the html result.
    if os.path.exists(restpath):
        layout_file = os.path.join('template.pt')
        layout = PageTemplate()
        layout.write(open(layout_file,"r").read())

        page = PageTemplate()
        page.write("""<metal:block use-macro="here/layout/macros/pagelayout" />""")

        context = Context(pageid)
        context.setRestContent(restpath)

        settings = {}
        settings["here"] = { "layout": layout }
        settings["context"] = context

        content = page.pt_render(namespace=settings)

        print content


if __name__ == '__main__':
    import sys
    args = sys.argv

    if len(args) < 2:
      print """  Usage: ./grok2html.py pageid restsource > pageid.html
      Prints to stdout the results of parsing restsource with grok template."""
    else:
        handler_html(args[1], args[2])
