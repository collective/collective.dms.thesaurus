#import datetime
from Acquisition import aq_parent
from zope.interface import implements

from zope import schema

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Item

from plone.supermodel import model

from . import _
from .keywordsfield import ThesaurusKeywords
from .equivalencesfield import ThesaurusKeywordEquivalences
from .vocabulary import NoThesaurusFound

class IDmsKeyword(model.Schema):
    """ """

    title = schema.TextLine(
        title=_(u"Title")
        )

    # EQ: equivalences
    equivs = ThesaurusKeywordEquivalences(
        title=_(u'EQ (Equivalences)'),
        required=False,
        )

    # BT: broader term
    broader = ThesaurusKeywords(
        title=_(u"BT (Broader Terms)"),
        required=False,
        vocabulary=u'dms.thesaurus.internalrefs'
        )

    # RT: related term
    related = ThesaurusKeywords(
        title=_(u"RT (Related Terms)"),
        required=False,
        display_backrefs=True,
        vocabulary=u'dms.thesaurus.internalrefs'
        )

    # HN: historical note
    historical_note = schema.Text(
        title=_(u"HN (Historical Note)"),
        required=False,
        )

    # SN: scope note
    scope_note = schema.Text(
        title=_(u"SN (Scope Note)"),
        required=False,
        )


class DmsKeyword(Item):
    """ """
    implements(IDmsKeyword)


class DmsKeywordSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsKeyword, )

