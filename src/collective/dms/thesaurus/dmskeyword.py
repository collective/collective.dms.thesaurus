import datetime
from zope import schema
#from zope.component import adapts
from zope.interface import implements

#from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy

from collective.dms.thesaurus.relateddocs import RelatedDocs

#from plone.supermodel import model

from collective.dms.thesaurus.dmsdocument import IDmsDocument, DmsDocument
from collective.contact.content.schema import ContactList, ContactChoice

from . import _

from plone.autoform import directives as form
from plone.directives.form import default_value

class IDmsKeyword(model.Schema):
    """ """

class DmsKeyword(DmsDocument):
    """ """
    implements(IDmsKeyword)


class DmsKeywordSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsKeyword, )


