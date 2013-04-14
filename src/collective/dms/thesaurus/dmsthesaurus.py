from zope.interface import implements

from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container

from plone.supermodel import model

from . import _

from .keywordsfield import ThesaurusKeywords

class IDmsThesaurus(model.Schema):
    """ """

    entry_points = ThesaurusKeywords(
        title=_(u"Entry Points"),
        description=_(u"First level of navigation for this Thesaurus"),
        vocabulary=u'dms.thesaurus.internalrefs',
        required=False)

class DmsThesaurus(Container):
    """ """
    implements(IDmsThesaurus)

class DmsThesaurusSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsThesaurus, )
