from zope.interface import implementer
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapter

from zope import schema
from zope.schema.interfaces import IChoice

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.form import form, button, field
from plone.z3cform import layout
#from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget


from plone.formwidget.autocomplete.widget import  AutocompleteBase, AutocompleteSelectionWidget
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget

#from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.dexterity.browser.view import DefaultView
#from Products.Five.browser import BrowserView

#from plone.dexterity.interfaces import IDexterityFTI
#from plone.dexterity.utils import getAdditionalSchemata

from collective.dms.thesaurus import _
from collective.dms.thesaurus.vocabulary import InternalThesaurusSource

class IAutocompleteSearchWidget(IAutocompleteWidget):
    """Simple autocomplete search input widget
    """

class AutocompleteSearchWidget(AutocompleteSelectionWidget):
    """Search widget with autocompletion.
    """
    implements(IAutocompleteSearchWidget)

    klass = u'autocomplete-search-widget'
    input_template = ViewPageTemplateFile('thesaurus_search_input.pt')
    display_template = ViewPageTemplateFile('thesaurus_search_input.pt')


@adapter(IAutocompleteSearchWidget, IFormLayer)
@implementer(IFieldWidget)
def AutocompleteSearchFieldWidget(field, request):
    return FieldWidget(field, AutocompleteSearchWidget(request))


class IThesaurusForm(Interface):
    keyword_search = schema.Choice(
        title=_(u"Quick Search"),
        description=_(u"Search for a keyword in this Thesaurus"),
        source=InternalThesaurusSource(), required=False)


class DmsThesaurusForm(form.Form):
    implements(IThesaurusForm)

    fields = field.Fields(IThesaurusForm)
    fields['keyword_search'].widgetFactory = AutocompleteSearchFieldWidget
    ignoreContext = True
    template = ViewPageTemplateFile('thesaurus_form.pt')

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

#from .searchform import SearchForm

class DmsThesaurusView(DefaultView):

    def renderForm(self):
        form = DmsThesaurusForm(self.context, self.request)
        #form = SearchForm(self.context, self.request)
        form.update()
        return form.render()
    