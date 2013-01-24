#import datetime
from zope.interface import implements, implementer, Interface
#from zope.component import adapts
from zope.component import adapter

from zope import schema
from zope.schema.interfaces import IList

from z3c.form.interfaces import IFormLayer, IFieldWidget, IMultiWidget
from z3c.form.widget import FieldWidget, MultiWidget

# #from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Item

from plone.supermodel import model
from plone.autoform.directives import widget

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

from . import _
from .relatedkeywords import RelatedThesaurusKeywords

#from plone.autoform import directives as form
#from plone.directives.form import default_value

class IEquivalences(IList):
    """"""

class Equivalences(schema.List):
    implements(IEquivalences)

    def __init__(self, **kwargs):
        schema.List.__init__(self, **kwargs)

@adapter(IEquivalences, IFormLayer)
@implementer(IFieldWidget)
def EquivalencesWidget(field, request):
    return FieldWidget(field, MultiWidget(request))

class IEquivalencesSchema(Interface):
    equiv = schema.TextLine(
            title=_("Equivalence"),
#            required=False,
            )


class IDmsKeyword(model.Schema):
    """ """

    equivs = schema.List(
        title=_(u"EQ (Equivalences)"),
        required=False,
        value_type=DictRow(title=_("Equivalence"),
                           schema=IEquivalencesSchema)
        )
    widget(equivs=DataGridFieldFactory)

    # BT: broader term
    broader = RelatedThesaurusKeywords(
        title=_(u"BT (Broader Terms)"),
        required=False,
        )

    # RT: related term
    related = RelatedThesaurusKeywords(
        title=_(u"RT (Related Terms)"),
        required=False,
        )


class DmsKeyword(Item):
    """ """
    implements(IDmsKeyword)


class DmsKeywordSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsKeyword, )


