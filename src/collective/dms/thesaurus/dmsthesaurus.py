#import datetime
#from zope import schema
#from zope.component import adapts
from zope.interface import implements

#from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container

from plone.supermodel import model

from . import _

#from plone.autoform import directives as form
#from plone.directives.form import default_value

class NoThesaurusFound(Exception):
    """No thesaurus found"""


class IDmsThesaurus(model.Schema):
    """ """

class DmsThesaurus(Container):
    """ """
    implements(IDmsThesaurus)

    @property
    def nav_entry_points(self):
        entry_ids = ["001157243"]
        return entry_ids


class DmsThesaurusSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsThesaurus, )


