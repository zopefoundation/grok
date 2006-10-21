from setuptools import setup, find_packages

setup(
    name='ldapaddressbook',
    version='0.1',
    author='Christian Theune',
    author_email='ct@gocept.com',
    url='http://svn.zope.org/repos/main/grok/trunk/',
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
