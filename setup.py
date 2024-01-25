import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
    )

tests_require = [
    'zope.app.wsgi[test]',
    'zope.configuration',
    'zope.testbrowser',
    'zope.testing',
    'zope.testrunner',
    ]

setup(
    name='grok',
    version='5.0a2',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grok',
    description='Grok: Now even cavemen can use Zope 3!',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'grokcore.annotation >= 1.6',
        'grokcore.catalog >= 2.1',
        'grokcore.chameleon >= 1.0',
        'grokcore.component >= 3.1',
        'grokcore.content >= 1.2',
        'grokcore.formlib >= 1.10',
        'grokcore.layout >= 1.6',
        'grokcore.message',
        'grokcore.security[role] >= 1.6',
        'grokcore.site >= 1.7',
        'grokcore.traverser >= 1.1',
        'grokcore.view [security_publication]',
        'grokcore.view >= 2.8',
        'grokcore.viewlet >= 1.10',
        'martian >= 1.2',
        'pytz',
        'setuptools',
        'z3c.autoinclude',
        'zc.catalog',
        'ZODB',
        'zope.annotation',
        'zope.app.appsetup',
        'zope.app.publication',
        'zope.app.wsgi',
        'zope.browserpage',
        'zope.catalog',
        'zope.component',
        'zope.container',
        'zope.contentprovider',
        'zope.errorview [browser]',
        'zope.event',
        'zope.exceptions',
        'zope.generations',
        'zope.i18n',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.intid',
        'zope.keyreference',
        'zope.lifecycleevent',
        'zope.location',
        'zope.login',
        'zope.password',
        'zope.principalregistry',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.securitypolicy',
        'zope.site',
        'zope.traversing',
        ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'docs': ['Sphinx']
    },
)
