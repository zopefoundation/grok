from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require = [
    'zope.app.wsgi',
    'zope.configuration',
    'zope.testing',
    ]

setup(
    name='grok',
    version='1.11.dev0',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://cheeseshop.python.org/pypi/grok/',
    description='Grok: Now even cavemen can use Zope 3!',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Framework :: Zope3',
        ],
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'grokcore.annotation >= 1.1',
        'grokcore.catalog',
        'grokcore.chameleon',
        'grokcore.component >= 2.3',
        'grokcore.content',
        'grokcore.formlib >= 1.4',
        'grokcore.json',
        'grokcore.layout',
        'grokcore.message',
        'grokcore.rest',
        'grokcore.security[role] >= 1.1',
        'grokcore.site > 1.4',
        'grokcore.traverser',
        'grokcore.view >= 2.6.1',
        'grokcore.viewlet >= 1.3',
        'grokcore.view [security_publication]',
        'grokcore.xmlrpc',
        'grokcore.catalog',
        'martian >= 0.14',
        'pytz',
        'setuptools',
        'simplejson',
        'z3c.autoinclude',
        'zc.catalog',
        'ZODB3',
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
    extras_require={'test': tests_require},
)
