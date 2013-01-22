# -*- coding: utf8 -*-

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.dms.thesaurus

class ThesaurusLayer(PloneWithPackageLayer):

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.dms.thesaurus:default')


COLLECTIVE_DMS_THESAURUS = ThesaurusLayer(
    zcml_package=collective.dms.thesaurus,
    zcml_filename='configure.zcml',
    gs_profile_id='collective.dms.thesaurus:default',
    name="COLLECTIVE_DMS_THESAURUS")

INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_DMS_THESAURUS, ),
    name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_DMS_THESAURUS, ),
    name="FUNCTIONAL")
