from setuptools import setup, find_packages

setup(
    name='addressbook',
    version='0.1',
    author='Christian Theune',
    author_email='ct@gocept.com',
    url='http://svn.gocept.com/grok-applications/addressbook/trunk',
    description="""\
Allows to edit addressbook entries of ~inetOrgPerson in LDAP
""",
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='ZPL',

    install_requires=['setuptools',
                     ],
)
