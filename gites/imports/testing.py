# -*- coding: utf-8 -*-
from plone.testing import zca
from plone.app.testing import layers
from plone.app.testing import PloneWithPackageLayer
import gites.imports


class PloneFixtureWithLinguaPlone(layers.PloneFixture):
    products = layers.PloneFixture.products + (
        ('Products.LinguaPlone', {'loadZCML': True}),
        ('gites.core', {'loadZCML': True}))


PLONE_FIXTURE_WITH_LINGUAPLONE = PloneFixtureWithLinguaPlone()

IMPORTS_FUNCTIONAL_BASE_LAYER = PloneWithPackageLayer(
    name='IMPORTS_FUNCTIONAL_BASE_LAYER',
    bases=(PLONE_FIXTURE_WITH_LINGUAPLONE, ),
    zcml_filename="testing.zcml",
    zcml_package=gites.imports,
    gs_profile_id='gites.imports:testing')

IMPORTS_FUNCTIONAL_LAYER = layers.FunctionalTesting(
    name='IMPORTS_FUNCTIONAL_LAYER',
    bases=(IMPORTS_FUNCTIONAL_BASE_LAYER, ))

IMPORTS_ZCML = zca.ZCMLSandbox(
    filename='testing.zcml',
    package=gites.imports,
    name='GITES_IMPORTS_ZCML')
