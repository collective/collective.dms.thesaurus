from zope.component import getUtility

from zope.app.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from plone.dexterity.browser.view import DefaultView

#from plone.dexterity.interfaces import IDexterityFTI
#from plone.dexterity.utils import getAdditionalSchemata


class DmsThesaurusView(DefaultView):
    """The default view for DMSThesaurus.
    """

