from zope.interface import implements, implementer
from zope.component import adapter

from zope import schema
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ISet
from zope.schema.interfaces import IFromUnicode

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget

from plone.formwidget.autocomplete.widget import AutocompleteMultiSelectionWidget

#from . import _

#from collective.dms.thesaurus.vocabulary import InternalThesaurusSource

class IEntryPointChoice(IChoice):
    """Thesaurus Entry Point Choice Item.
    """

class EntryPointChoice(schema.Choice):
    implements(IEntryPointChoice, IFromUnicode)

class IEntryPoints(ISet):
    """Thesaurus Entry Point List.
    """

class EntryPoints(schema.Set):
    implements(IEntryPoints, IFromUnicode)

    def __init__(self, **kw):
        vt = kw.pop('value_type',
                    schema.Choice(
                            required=False,
                            vocabulary=u'dms.thesaurus.internalrefs')
                    )
        super(EntryPoints, self).__init__(value_type=vt, **kw)


class EntryPointsWidget(AutocompleteMultiSelectionWidget):

    klass = u"entrypoints-widget"
    display_template = ViewPageTemplateFile('entrypoints_display.pt')
    maxResults = 50

    #def __init__(self, request):
    #    super(EntryPointsWidget, self).__init__(request)

    def items(self):
        value = []
        for token in self.value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue
            term = self.terms.getTermByToken(token)
            value.append({'id': token, 'value': term.value,
                          'content': term.title, 'selected': True
                          })
        return value

    def displayItems(self):
        path = '/'.join(self.context.getPhysicalPath())
        value = []
        for token in self.value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue
            term = self.terms.getTermByToken(token)
            value.append(
                {'title': term.title,
                 'href': '/'.join((path, term.value))
                 })
        return value

@adapter(IEntryPoints, IFormLayer)
@implementer(IFieldWidget)
def EntryPointsFieldWidget(field, request):
    return FieldWidget(field, EntryPointsWidget(request))

