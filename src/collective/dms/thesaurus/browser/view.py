from zope.component import getUtility

from zope.app.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from plone.dexterity.browser.view import DefaultView

#from plone.dexterity.interfaces import IDexterityFTI
#from plone.dexterity.utils import getAdditionalSchemata


class DmsKeywordView(DefaultView):
    """The default view for DMSKeyword.
    """

    @property
    def children(self):
        intids = getUtility(IIntIds)
        catalog = getUtility(ICatalog)
        value = []
        try:
            doc_intid = intids.getId(self.context)
        except KeyError:
            pass
        else:
            for ref in catalog.findRelations(
                    {'to_id': doc_intid, 'from_attribute': 'broader'}):
                tp = (ref.from_path, ref.from_object.Title())
                if tp not in value:
                    value.append(tp)
        return value

