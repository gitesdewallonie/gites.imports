# -*- coding: utf-8 -*-
import json
import unittest2 as unittest
from plone import api
from gites.imports import testing
from plone.app.testing import setRoles, TEST_USER_NAME, TEST_USER_ID
from plone.app.testing.helpers import login


class PackagesSyncTest(unittest.TestCase):
    layer = testing.GITES_IMPORTS_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        request = self.layer['request']
        self.export_packages_view = api.content.get_view(
            name='export_packages',
            context=portal,
            request=request)

    def test_site_without_package(self):
        data = json.loads(self.export_packages_view())
        self.assertEqual([], data)

    def test_site_with_one_package(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        api.content.create(
            type='Image',
            id='img1',
            title='My Image',
            container=portal)
        package = api.content.create(
            type='Package',
            title='My Package',
            container=portal)
        api.content.transition(obj=package, transition='publish')
        data = json.loads(self.export_packages_view())
        self.assertNotEqual([], data)
        self.assertEqual(len(data), 1)
        self.assertTrue(type(data[0]) is dict)
        self.assertEqual(data[0]['title'], u'My Package')
        self.assertTrue('hebergements' in data[0])

    def test_site_with_one_package_and_one_image(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        package = api.content.create(
            type='Package',
            title='My Package',
            container=portal)
        api.content.transition(obj=package, transition='publish')
        api.content.create(
            type='Image',
            id='img1',
            title='My Image',
            container=package)
        api.content.create(
            type='Vignette',
            id='vign1',
            title='My Vignette',
            container=package)
        data = json.loads(self.export_packages_view())
        self.assertNotEqual([], data)
        self.assertEqual(len(data), 3)
