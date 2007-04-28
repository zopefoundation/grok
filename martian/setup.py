from setuptools import setup, find_packages

setup(
    name='martian',
    version='0.1',
    author='Grok project',
    author_email='grok-dev@zope.org',
    description="""\
Martian is a library that allows the embedding of configuration
information in Python code. Martian can then grok the system and
do the appropriate configuration registrations. One example of a system
that uses Martian is the system where it originated: Grok
(http://grok.zope.org)
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='ZPL',
    install_requires=[
    'zope.interface',
    'setuptools',
    ],
)
