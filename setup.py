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
    'zope.app.testing',
    'zope.configuration',
    'zope.testbrowser',
    'zope.testing',
    ]

setup(
    name='grok',
    version='1.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://cheeseshop.python.org/pypi/grok/',
    description='Grok: Now even cavemen can use Zope 3!',
    long_description=long_description,
    license='ZPL',
    classifiers=['Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    install_requires=['setuptools',
                      'ZODB3',
                      'grokcore.annotation >= 1.1',
                      'grokcore.component >= 1.5, < 2.0',
                      'grokcore.formlib >= 1.4',
                      'grokcore.security >= 1.1',
                      'grokcore.site',
                      'grokcore.content',
                      'grokcore.view >= 1.12',
                      'grokcore.viewlet >= 1.3',
                      'martian >= 0.10, < 0.12',
                      'pytz',
                      'simplejson',
                      'z3c.autoinclude',
                      'z3c.flashmessage',
                      'z3c.testsetup',
                      'zc.catalog',
                      'zope.annotation',
                      'zope.app.publication',
                      'zope.app.publisher',
                      'zope.app.renderer',
                      'zope.app.zcmlfiles',
                      'zope.catalog',
                      'zope.component',
                      'zope.container',
                      'zope.contentprovider',
                      'zope.copypastemove',
                      'zope.event',
                      'zope.exceptions',
                      'zope.formlib',
                      'zope.i18n',
                      'zope.interface',
                      'zope.intid',
                      'zope.keyreference',
                      'zope.lifecycleevent',
                      'zope.location',
                      'zope.password',
                      'zope.pluggableauth',
                      'zope.publisher',
                      'zope.schema',
                      'zope.security',
                      'zope.securitypolicy',
                      'zope.site',
                      'zope.size',
                      'zope.traversing',
                      # Reported as unused by z3c.dependencychecker.  Should
                      # be removed or moved to the deprecated packages list.
                      'zope.app.appsetup',
                      'zope.app.pagetemplate',
                      'zope.app.security',
                      'zope.app.twisted',
                      'zope.deprecation',
                      'zope.dottedname',
                      'zope.hookable',
                      'zope.i18nmessageid',
                      'zope.pagetemplate',
                      'zope.proxy',
                      'zope.viewlet',
                      ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
