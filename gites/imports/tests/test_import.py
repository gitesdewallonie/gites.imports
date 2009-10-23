# -*- coding: utf-8 -*-
"""
gites.import

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: event.py 67630 2006-04-27 00:54:03Z jfroche $
"""
from Products.CMFPlone.tests.PloneTestCase import FunctionalTestCase
from zope.app.component.hooks import setHooks
from Products.PloneTestCase.layer import PloneSite, onsetup
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
import unittest
from zope.testing import doctest, cleanup
from Products.Five import zcml
import tempfile
import shutil
import os
from collective.transmogrifier.transmogrifier import configuration_registry


BASEDIR = None


def registerConfig(name, configuration):
    filename = os.path.join(BASEDIR, '%s.cfg' % name)
    open(filename, 'w').write(configuration)
    configuration_registry.registerConfiguration(
        name,
        u"Pipeline configuration '%s' from "
        u"'collective.transmogrifier.tests'" % name,
        u'', filename)


from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

UNITTESTS = []

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE|
               doctest.REPORT_ONLY_FIRST_FAILURE)

linguaPloneHook = """
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
    xmlns:five="http://namespaces.zope.org/five">

  <five:registerPackage package="Products.LinguaPlone"
                        initialize="Products.LinguaPlone.initialize" />

</configure>
"""
excludeProfiles = """
<configure xmlns="http://namespaces.zope.org/zope"
  i18n_domain="gites">

  <exclude package="gites.imports" file="profiles.zcml"/>

</configure>
"""


@onsetup
def setupPackages():
    import zc.configuration
    zcml.load_config('meta.zcml', zc.configuration)
    import Products.LinguaPlone
    zcml.load_string(linguaPloneHook)
    zcml.load_config('configure.zcml', Products.LinguaPlone)
    import five.grok
    zcml.load_config('meta.zcml', five.grok)
    zcml.load_config('configure.zcml', five.grok)
    import z3c.amf
    zcml.load_config('meta.zcml', z3c.amf)
    zcml.load_config('configure.zcml', z3c.amf)
    import gites.core
    zcml.load_config('configure.zcml', gites.core)
    import gites.db
    zcml.load_config('configure.zcml', gites.db)
    import gites.imports
    zcml.load_string(excludeProfiles)
    zcml.load_config('configure.zcml', gites.imports)

    ztc.installPackage('gites.core')
    ztc.installPackage('gites.imports')
    ztc.installPackage('Products.LinguaPlone')

setupPackages()
ptc.setupPloneSite(products=['gites.imports',
                             'gites.core',
                             'Products.LinguaPlone'])


class GitesImportZCMLLayer(PloneSite):

    @classmethod
    def setUp(cls):
        import Products
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('event.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.Five)
        setHooks()
        import Products.LinguaPlone
        zcml.load_string(linguaPloneHook)
        zcml.load_config('configure.zcml', Products.LinguaPlone)
        global BASEDIR
        BASEDIR = tempfile.mkdtemp('transmogrifierTestConfigs')
        import plone.app.transmogrifier
        import Products.Five
        zcml.load_config('configure.zcml', Products.Five)
        import Products.GenericSetup
        zcml.load_config('meta.zcml', Products.GenericSetup)
        zcml.load_config('configure.zcml', plone.app.transmogrifier)
        import gites.imports
        zcml.load_config('configure.zcml', gites.imports)

    @classmethod
    def tearDown(cls):
        shutil.rmtree(BASEDIR)
        cleanup.cleanUp()


class GitesImportFunctionalTestCase(FunctionalTestCase):
    layer = GitesImportZCMLLayer


def test_suite():
    suites = [Suite('../gitesimport.txt',
               optionflags=OPTIONFLAGS,
               package='gites.imports.tests',
               test_class=GitesImportFunctionalTestCase)]
    return unittest.TestSuite(suites)
