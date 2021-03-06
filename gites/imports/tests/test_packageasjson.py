# -*- coding: utf-8 -*-
import json
import os
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
        ideeSejour = getattr(portal, 'idee-sejour')
        package = api.content.create(
            type='Package',
            id='package1',
            title='My Package',
            container=ideeSejour)
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
        ideeSejour = getattr(portal, 'idee-sejour')
        package = api.content.create(
            type='Package',
            id='package1',
            title='My Package',
            container=ideeSejour)
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
        raw_data = self.export_packages_view()
        if 'DUMP_FILE' in os.environ:
            with open(testing.PACKAGE_TEST_PATH, 'w') as fd:
                fd.write(raw_data)
        data = json.loads(raw_data)
        self.assertNotEqual([], data)
        self.assertEqual(len(data), 3)
