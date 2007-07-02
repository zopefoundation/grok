import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='megrok.viewlet',
    version='0.1',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://svn.zope.org/grok/trunk',
    description="""\
Grok: Now even cavemen can use Zope3!
""",
    long_description=(
        read('src/megrok/viewlet/README.txt')
        ),
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    zip_safe=False,
    license='ZPL',

    install_requires=['setuptools',
                      'zope.viewlet',
                      'z3c.viewlet',
                      'megrok.view',
                     ],
)

