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
        return []
        """
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
                tp = dict(
                    url=ref.from_path,
                    label=ref.from_object.Title(),
                    hn=ref.from_object.historical_note,
                    sn=ref.from_object.scope_note
                    )
                if tp not in value:
                    value.append(tp)
        return value

        """
