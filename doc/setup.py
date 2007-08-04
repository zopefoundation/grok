from setuptools import setup, find_packages

setup(
    name='grokdocs',
    install_requires=['docutils',
                      'zope.pagetemplate',
                      'zope.app.renderer',
                      'Pygments'
                      ],
    py_modules = ['grok2html'],
    entry_points="""
    [console_scripts]
    grok2html = grok2html:main
    """
    )
