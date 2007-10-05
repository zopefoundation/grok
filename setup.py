from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='grokdoctool',
      version=version,
      description="Generate html pages out of rst python documentation files",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='rst html python doc grok',
      author='Grok Team',
      author_email='',
      url='grok.zope.org',
      license='',
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=['docutils', 'lxml'],
      entry_points={'console_scripts':['grokdoctool=grokdoctool.rst2html:main']}
      )
