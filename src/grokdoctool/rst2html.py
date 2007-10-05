import sys
import os
from optparse import OptionParser
from docutils.core import publish_string

# import modules from python core doc generation code
# these modules will register extensions in docutils
from  extensions import addnodes, directives, roles

try:
    from lxml import etree
except:
    etree = None

XSLT_FILE = os.path.join(os.path.split(__file__)[0], 'grok.xslt')

class ReST2HTML(object):
    def __init__(self, inputdir, xslt_file=None):
       self.inputdir = inputdir
       self.xslt_file = xslt_file

    def _walk(self):
        for rootpath, directories, files in os.walk(self.inputdir):
            if '.svn' in directories:
                directories.remove('.svn')
            for file in files:
                if file.startswith('.'):
                    continue
                if not os.path.splitext(file)[1] in ['.rst', '.txt']:
                    continue
                yield os.path.join(rootpath, file)

    def run(self):
        for path in self._walk():
            directory, rst_file = os.path.split(path)
            html_file = os.path.splitext(rst_file)[0] + '.html'
            sys.stderr.write('%s\n' % rst_file)
            self.convert_file(path, os.path.join(directory, html_file))

    def convert_file(self, rst_file, html_file):
        fp = open(rst_file)
        input = fp.read()
        fp.close()
        output = publish_string(input,
                                rst_file,
                                writer_name='xml')
        if self.xslt_file:
            input_doc = etree.fromstring(output)
            transform = etree.XSLT(etree.parse(self.xslt_file))
            output_doc = transform(input_doc)
            output = etree.tostring(output_doc, pretty_print=True)
        if output:
            fp = open(html_file, 'w')
            fp.write(output)
            fp.close()

def main():
    usage = "usage: %prog INPUTDIR"
    parser = OptionParser(usage)

    parser.add_option('-x', '--xslt', dest="xslt_file",
                       help="use a specific xslt stylesheet",
                       metavar='XSTLFILE')

    options, args = parser.parse_args()

    if not len(args) == 1:
        sys.stderr.write('%s\n' % usage)
        sys.exit(1)

    inputdir = args[0]

    if not os.path.isdir(inputdir):
        sys.stderr.write('input directory %s does not exist\n' % inputdir)
        sys.exit(1)
    
    xslt_file = None
    if etree:
        xslt_file = options.xslt_file or XSLT_FILE

    ReST2HTML(inputdir, xslt_file=xslt_file).run()

if __name__ == '__main__':
    main()
