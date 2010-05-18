from setuptools import setup, find_packages

setup(
    name='grokwiki',
    version='0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://svn.zope.org/grok/trunk',
    description="""\
Grok: Now even cavemen can use wikis!
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='ZPL',

    install_requires=['setuptools',
                      'grok',
                      'grokui.admin',
                      'grokcore.startup',
                      'grokcore.message',
                      ],
    entry_points = """
      [console_scripts]
      grokwiki-debug = grokcore.startup:interactive_debug_prompt
      grokwiki-ctl = grokcore.startup:zdaemon_controller
      [paste.app_factory]
      main = grokcore.startup:application_factory
      """,
)
