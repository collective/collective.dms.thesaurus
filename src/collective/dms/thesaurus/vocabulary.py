from zope.interface import Interface
from zope.interface import implements
from five import grok

from zope.schema.interfaces import IContextSourceBinder

#from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
#from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
#from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName


class IMainThesaurus(Interface):
    """ Marker interface for main thesaurus container
    """

class ThesaurusVocabulary(SimpleVocabulary):

    def search(self, query_string):
        q = query_string.lower()
        return [kw for kw in self._terms if q in kw.title.lower()]


class InternalThesaurusSource(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        results = catalog(portal_type='dmskeyword',
                          path={'query': path,'depth': 1})
        keywords = [x.getObject() for x in results]
        def cmp_keyword(x, y):
            return cmp(x.title, y.title)
        keywords.sort(cmp_keyword)
        #keyword_ids = [x.id for x in keywords]
        _c = SimpleVocabulary.createTerm
        keyword_terms = [ _c(x.id, x.id, x.title) for x in keywords ]
        return ThesaurusVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


class GlobalThesaurusSource(object):
    implements(IContextSourceBinder)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword')
        keywords = [x.getObject() for x in results]
        def cmp_keyword(x, y):
            return cmp(x.title, y.title)
        keywords.sort(cmp_keyword)
        #keyword_ids = [x.id for x in keywords]
        keyword_terms = [SimpleVocabulary.createTerm(
                                x.id, x.id, x.title) for x in keywords]
        return ThesaurusVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


#grok.global_utility(GlobalThesaurusSource,
#                    name=u'dms.thesaurus.global')


class KeywordFromSameThesaurusSource(object):
    """
    This vocabulary is used for keywords that reference one another
    inside the same thesaurus. It should not be used for referencing
    keywords from other content types.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        if context.portal_type == 'dmsthesaurus':
            thesaurus_path = '/'.join(context.getPhysicalPath())
        else:
            thesaurus_path = '/'.join(context.thesaurusPath())
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword',
                          path={'query': thesaurus_path,'depth': 1})
        keywords = [x.getObject() for x in results]
        def cmp_keyword(x, y):
            return cmp(x.title, y.title)
        keywords.sort(cmp_keyword)

        keyword_ids = [x.id for x in keywords]
        keyword_terms = [SimpleVocabulary.createTerm(
                                x.id, x.id, x.title) for x in keywords]
        return SimpleVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


grok.global_utility(KeywordFromSameThesaurusSource,
                    name=u'dms.thesaurus.internalrefs')
