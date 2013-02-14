from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='gites.imports',
      version=version,
      description="Import Content for Gites using transmogrifier",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gites'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.transmogrifier',
          'collective.blueprint.translationlinker',
          'collective.blueprint.downloader',
          'Plone',
          'Products.LinguaPlone',
          'zc.configuration',
          'zc.datetimewidget',
          'five.grok',
          'gites.core',
          'gites.skin',
      ],
      extras_require={
        'test': [
            'unittest2',
            'plone.app.testing']})
