from Products.CMFCore.utils import getToolByName
from plone.dexterity.browser.view import DefaultView

class DmsKeywordView(DefaultView):
    """The default view for DMSKeyword.
    """

    @property
    def children(self):
        """
        Search in catalog for keywords that have context as broader term.
        Query is restricted to same thesaurus.
        Returns a list of dicts with ``url`` and ``label`` attributes.
        """
        thesaurus_path = '/'.join(self.context.thesaurusPath())
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type='dmskeyword',
            path={'query': thesaurus_path,'depth': 1},
            broaderThesaurusKeywords=self.context.id)
        refs = []
        for ref in brains:
            if ref.id != self.context.id:
                refs.append({'url':ref.getPath(), 'label':ref.Title})
        def cmp_ref(x, y):
            return cmp(x['label'], y['label'])
        refs.sort(cmp_ref)
        return refs

    @property
    def related(self):
        """
        Search in catalog for keywords that have context as broader term.
        Query is restricted to same thesaurus.
        Returns a list of dicts with ``url`` and ``label`` attributes.
        """
        refs = []
        related = self.context.related
        thesaurus = self.context.thesaurus()
        thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
        for ref in related:
            kw = getattr(thesaurus, ref)
            refs.append({'url': '/'.join(kw.getPhysicalPath()),
                         'label': kw.Title()})
        catalog = getToolByName(self.context, 'portal_catalog')
        brains =  catalog.searchResults(
                        portal_type='dmskeyword',
                        path={'query': thesaurus_path,'depth': 1},
                        relatedThesaurusKeywords=self.context.id
                        )
        for brain in brains:
            ref = {'url':brain.getPath(), 'label':brain.Title}
            if brain.id != self.context.id and ref not in refs:
                refs.append(ref)
        def cmp_ref(x, y):
            return cmp(x['label'], y['label'])
        refs.sort(cmp_ref)
        return refs
