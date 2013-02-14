# -*- coding: utf-8 -*-
import doctest
import os
import tempfile
import unittest2 as unittest
from plone.testing import layered
from gites.imports import testing
from collective.transmogrifier.transmogrifier import configuration_registry


BASEDIR = tempfile.mkdtemp('transmogrifierTestConfigs')


def registerConfig(name, configuration):
    filename = os.path.join(BASEDIR, '%s.cfg' % name)
    open(filename, 'w').write(configuration)
    configuration_registry.registerConfiguration(
        name,
        u"Pipeline configuration '%s' from "
        u"'collective.transmogrifier.tests'" % name,
        u'', filename)


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('gitesimport.txt', package='gites.imports',
                                     optionflags=OPTIONFLAGS),
                layer=testing.GITES_IMPORTS_FUNCTIONAL),
    ])
    return suite
