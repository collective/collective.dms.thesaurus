from zope.interface import Interface
from five import grok

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName

import utils

class NoThesaurusFound(Exception):
    """No thesaurus found"""


class IMainThesaurus(Interface):
    """ Marker interface for main thesaurus container
    """

class SimpleThesaurusSource(object):
    """This basic vocabulary is here mainly for demo purpose.
    It is not meant to be used when a Plone site contains more than one
    thesaurus.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        # build vocab from first thesaurus returned by catalog
        thesaurus = utils.get_thesaurus_object(context)
        if thesaurus is None:
            return SimpleVocabulary([])
        thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword',
                          path={'query': thesaurus_path,'depth': 1})
        keyword_terms = [SimpleVocabulary.createTerm(
                                x.getId, x.getId, x.Title) for x in results]
        return SimpleVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


grok.global_utility(SimpleThesaurusSource,
                    name=u'dms.thesaurus.simple')


class KeywordFromSameThesaurusSource(object):
    """This vocabulary is used for keywords that reference one another
    inside the same thesaurus. It should not be used for referencing
    keywords from other content types.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        if context.portal_type == 'dmsthesaurus':
            thesaurus_path = '/'.join(context.getPhysicalPath())
        else:
            thesaurus = utils.get_thesaurus_object(context)
            if thesaurus is None:
                return SimpleVocabulary([])
            thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword',
                          path={'query': thesaurus_path,'depth': 1})
        keyword_terms = [SimpleVocabulary.createTerm(
                                x.getId, x.getId, x.Title) for x in results]
        return SimpleVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


grok.global_utility(KeywordFromSameThesaurusSource,
                    name=u'dms.thesaurus.internalrefs')
