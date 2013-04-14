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

class GlobalThesaurusSource(object):
    """This basic vocabulary is here mainly for demo purpose.
    It is not meant to be used when a Plone site contains more than one
    thesaurus.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        thesaurus = catalog(portal_type='dmsthesaurus')
        if not len(thesaurus):
            raise NoThesaurusFound
        # build vocab from first thesaurus returned by catalog
        thesaurus_path = '/'.join(thesaurus[0].getPath())
        results = catalog(portal_type='dmskeyword',
                          path={'query': thesaurus_path,'depth': 1})
        keywords = [x.getObject() for x in results]
        keyword_terms = [SimpleVocabulary.createTerm(
                                x.id, x.id, x.title) for x in keywords]
        return SimpleVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


grok.global_utility(GlobalThesaurusSource,
                    name=u'dms.thesaurus.global')


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
            thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(portal_type='dmskeyword',
                          path={'query': thesaurus_path,'depth': 1})
        keywords = [x.getObject() for x in results]

        keyword_terms = [SimpleVocabulary.createTerm(
                                x.id, x.id, x.title) for x in keywords]
        return SimpleVocabulary(keyword_terms)

    def __iter__(self):
        # hack to let schema editor handle the field
        yield u'DO NOT TOUCH'


grok.global_utility(KeywordFromSameThesaurusSource,
                    name=u'dms.thesaurus.internalrefs')
