from zope import schema
from zope.interface import Interface

from z3c.form import form, button, field
#from plone.z3cform import layout
#from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from plone.dexterity.browser.view import DefaultView
#from Products.Five.browser import BrowserView

#from plone.dexterity.interfaces import IDexterityFTI
#from plone.dexterity.utils import getAdditionalSchemata

from collective.dms.thesaurus.vocabulary import InternalThesaurusSource


class IThesaurusForm(Interface):
    keyword_search = schema.Choice(title=u"Search for keyword",
        source=InternalThesaurusSource(), required=False)


class DmsThesaurusForm(form.Form):
    fields = field.Fields(IThesaurusForm)
    #fields['keyword_search'].widgetFactory = AutocompleteFieldWidget
    ignoreContext = True
    template = ViewPageTemplateFile('thesaurus_form.pt')

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors

class DmsThesaurusView(DefaultView):

    def renderForm(self):
        form = DmsThesaurusForm(self.context, self.request)
        form.update()
        return form.render()
    