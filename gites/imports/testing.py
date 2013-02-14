# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import gites.imports


GITES_IMPORTS = PloneWithPackageLayer(
    zcml_package=gites.imports,
    zcml_filename='testing.zcml',
    gs_profile_id='gites.imports:testing',
    name="GITES_IMPORTS")

GITES_IMPORTS_INTEGRATION = IntegrationTesting(
    bases=(GITES_IMPORTS, ),
    name="GITES_IMPORTS_INTEGRATION")

GITES_IMPORTS_FUNCTIONAL = FunctionalTesting(
    bases=(GITES_IMPORTS, ),
    name="GITES_IMPORTS_FUNCTIONAL")
