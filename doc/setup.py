from setuptools import setup, find_packages

setup(
    name='grokdocs',
    install_requires=['docutils',
                      'zope.pagetemplate',
                      'zope.app.renderer',
                      'Pygments',
                      'ulif.rest',
                      ],
    package_dir = {'': 'build'},
    py_modules = ['grok2html', 'grokdocs'],
    entry_points="""
    [console_scripts]
    grokdocs2html = grokdocs:grokdocs
    grokdocs2latex = grokdocs:grokdocs_latex
    """
    )
