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
    version='1.4dev',
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
        'ZODB3',
        'grokcore.annotation >= 1.1',
        'grokcore.component >= 2.1',
        'grokcore.content',
        'grokcore.formlib >= 1.4',
        'grokcore.json',
        'grokcore.message',
        'grokcore.security >= 1.1',
        'grokcore.site',
        'grokcore.view',
        'grokcore.view [security_publication]',
        'grokcore.viewlet >= 1.3',
        'martian >= 0.14',
        'pytz',
        'setuptools',
        'simplejson',
        'z3c.autoinclude',
        'zc.catalog',
        'zope.annotation',
        'zope.app.appsetup',
        'zope.app.http',
        'zope.app.publication',
        'zope.browserpage',
        'zope.catalog',
        'zope.component',
        'zope.container',
        'zope.contentprovider',
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
