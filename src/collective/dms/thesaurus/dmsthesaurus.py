#import datetime
from zope import schema
#from zope.component import adapts
from zope.interface import implements
from zope.component import adapter
from zope.interface import implementer
from z3c.form.widget import FieldWidget, SequenceWidget

#from plone.dexterity.content import Container
from plone.dexterity.schema import DexteritySchemaPolicy
from plone.dexterity.content import Container

from zope.schema.interfaces import ISet
from zope.schema.interfaces import IFromUnicode
from z3c.form.interfaces import IFormLayer, IFieldWidget, ISequenceWidget

from plone.formwidget.autocomplete.widget import AutocompleteMultiSelectionWidget

from plone.supermodel import model

from . import _

from vocabulary import GlobalThesaurusSource

#from plone.autoform import directives as form
#from plone.directives.form import default_value

class NoThesaurusFound(Exception):
    """No thesaurus found"""


class IEntryPoints(ISet):
    pass

class EntryPoints(schema.Set):
    implements(IEntryPoints, IFromUnicode)


@adapter(IEntryPoints, IFormLayer)
@implementer(IFieldWidget)
def EntryPointsFieldWidget(field, request):
    return FieldWidget(field, AutocompleteMultiSelectionWidget(request))


class IDmsThesaurus(model.Schema):
    """ """

    entry_points = EntryPoints(
        title=_(u"Entry Points"),
        value_type=schema.Choice(source=GlobalThesaurusSource())
        )


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


