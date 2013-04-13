#import datetime
#from zope import schema
#from zope.component import adapts
from zope.interface import implements
#from zope.component import adapter
#from zope.interface import implementer
#from z3c.form.widget import FieldWidget, SequenceWidget

#from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container

#from zope.schema.interfaces import ISet
#from zope.schema.interfaces import IFromUnicode
#from z3c.form.interfaces import IFormLayer, IFieldWidget, ISequenceWidget


from plone.supermodel import model

from . import _

from .entrypointsfield import EntryPoints

#from plone.autoform import directives as form
#from plone.directives.form import default_value

class NoThesaurusFound(Exception):
    """No thesaurus found"""

class IDmsThesaurus(model.Schema):
    """ """

    entry_points = EntryPoints(
        title=_(u"Entry Points"),
        description=_(u"First level of navigation for this Thesaurus"),
        required=False)

class DmsThesaurus(Container):
    """ """
    implements(IDmsThesaurus)

class DmsThesaurusSchemaPolicy(DexteritySchemaPolicy):
    """ """

    def bases(self, schemaName, tree):
        return (IDmsThesaurus, )
