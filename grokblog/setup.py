from setuptools import setup, find_packages

setup(
    name='grokblog',
    version='0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://svn.zope.org/grok/trunk',
    description="""\
Grok: the blog
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='ZPL',

    install_requires=['setuptools',
                     ],
)
