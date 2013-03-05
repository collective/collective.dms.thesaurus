from zope.interface import Interface
#from zope.interface import implements
from five import grok

#from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
#from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
#from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName


class IMainThesaurus(Interface):
    """ Marker interface for main thesaurus container
    """


class GlobalThesaurusSource(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword')
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


grok.global_utility(GlobalThesaurusSource,
                    name=u'dms.thesaurus.global')

class KeywordFromSameThesaurusSource(object):
    """
    This vocabulary is used for keywords that reference one another
    inside the same thesaurus. It should not be used for referencing
    keywords from other content types.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
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
