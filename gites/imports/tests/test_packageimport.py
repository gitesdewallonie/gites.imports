# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch
from gites.imports import testing
from gites.imports.service import sync_packages
from gites.imports.blueprint.remotejsonsource import RemoteJsonSourceSection


class PackagesSyncTest(unittest.TestCase):
    layer = testing.GITES_IMPORTS_INTEGRATION

    def test_dummy_sync(self):
        def get_data(self):
            return [{'foo': 'bar'}]
        with patch.object(RemoteJsonSourceSection, '_get_data', new=get_data):
            sync_packages(input=None)
