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
                      ],
)
