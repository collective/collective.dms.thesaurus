#import datetime
from zope.interface import implements

from zope import schema

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Item

from plone.supermodel import model

from . import _
from .relatedkeywords import RelatedThesaurusKeywords
from .broaderkeywords import BroaderThesaurusKeywords
from .equivalences import ThesaurusKeywordEquivalences

class IDmsKeyword(model.Schema):
    """ """

    # EQ: equivalences
    equivs = ThesaurusKeywordEquivalences(
        title=u'EQ (Equivalences)',
        required=False,
        )

    # BT: broader term
    broader = BroaderThesaurusKeywords(
        title=_(u"BT (Broader Terms)"),
        required=False,
        )

    # RT: related term
    related = RelatedThesaurusKeywords(
        title=_(u"RT (Related Terms)"),
        required=False,
        display_backrefs=True
        )

    # HN: historical note
    historical_note = schema.Text(
        title=_(u"Historical Note"),
        required=False,
        )

    # SN: scope note
    scope_note = schema.Text(
        title=_(u"Scope Note"),
        required=False,
        )


class DmsKeyword(Item):
    """ """
    implements(IDmsKeyword)


class DmsKeywordSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsKeyword, )

