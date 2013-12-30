# -*- coding: utf-8 -*-
import unittest2
from collective.transmogrifier.transmogrifier import Transmogrifier
from Products.CMFCore.utils import getToolByName
from gites.imports import testing


class TestPackage(unittest2.TestCase):
    layer = testing.IMPORTS_FUNCTIONAL_LAYER

    def test_transmogrifier(self):
        portal = self.layer['portal']
        transmogrifier = Transmogrifier(portal)
        transmogrifier(u'gites.import.packages')
        ideesejourFolder = getattr(portal, 'idee-sejour')
        self.failUnless(len(ideesejourFolder.objectIds()) > 0)
        mice = getattr(ideesejourFolder, 'mice')
        self.assertEqual(mice.Title(), 'Séminaire au Vert')
        workflow = getToolByName(portal, 'portal_workflow')
        self.assertEqual(workflow.getInfoFor(mice, 'review_state'),
                         'published')
