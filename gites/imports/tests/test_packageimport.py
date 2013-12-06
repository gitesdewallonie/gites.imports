# -*- coding: utf-8 -*-
import json
import unittest2 as unittest
from mock import patch
from gites.imports import testing
from gites.imports.service import sync_packages
from gites.imports.blueprint.remotejsonsource import RemoteJsonSourceSection


class PackagesSyncTest(unittest.TestCase):
    layer = testing.GITES_IMPORTS_INTEGRATION

    def test_dummy_sync(self):
        def get_data(self):
            return []
        with patch.object(RemoteJsonSourceSection, '_get_data', new=get_data):
            sync_packages(input=None)

    def test_add_data(self):
        def get_data(self):
            with open(testing.PACKAGE_TEST_PATH) as fd:
                raw_data = fd.read()
                data = json.loads(raw_data)
            return data
        with patch.object(RemoteJsonSourceSection, '_get_data', new=get_data):
            sync_packages(input=None)
        portal = self.layer['portal']
        self.assertTrue('my-package' in portal.objectIds())
        package = getattr(portal, 'my-package')
        self.assertEqual(package.Title(), u'My Package')
        self.assertTrue('my-image' in package.objectIds())
        self.assertTrue('my-vignette' in package.objectIds())
