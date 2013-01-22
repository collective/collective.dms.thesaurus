# -*- coding: utf8 -*-

import unittest2 as unittest
#import datetime

from plone.app.testing import setRoles, TEST_USER_ID
from collective.dms.thesaurus.testing import INTEGRATION
#from collective.dms.thesaurus import keyword

class TestContentTypes(unittest.TestCase):
    """Base class to test new content types"""

    layer = INTEGRATION

    def setUp(self):
        super(TestContentTypes, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])


class TestThesaurusContentTypes(TestContentTypes):

    def test_something(self):
        pass
