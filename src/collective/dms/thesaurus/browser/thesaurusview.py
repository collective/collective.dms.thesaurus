from zope.interface import implementer
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapter

from zope import schema
from zope.schema.interfaces import IChoice

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form.interfaces import IFormLayer, IFieldWidget, ITextWidget
from z3c.form.widget import FieldWidget
from z3c.form import form, button, field
from plone.z3cform import layout
from z3c.form.browser import text
#from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget


from plone.formwidget.autocomplete.widget import  AutocompleteBase, AutocompleteSelectionWidget
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget

#from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.dexterity.browser.view import DefaultView
#from Products.Five.browser import BrowserView

#from plone.dexterity.interfaces import IDexterityFTI
#from plone.dexterity.utils import getAdditionalSchemata

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary


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


class IKeywordSearchWidget(ITextWidget):
    pass

class KeywordSearchWidget(text.TextWidget):
    implements(IKeywordSearchWidget)
    klass = u'keyword-search'

def KeywordSearchFieldWidget(field, request):
    return FieldWidget(field, KeywordSearchWidget(request))

class IThesaurusForm(Interface):
    keyword_search = schema.TextLine(
        title=_(u"Quick Search"),
        description=_(u"Search for a keyword in this Thesaurus"),
        required=False)


class DmsThesaurusForm(form.Form):
    implements(IThesaurusForm)

    fields = field.Fields(IThesaurusForm)
    fields['keyword_search'].widgetFactory = KeywordSearchFieldWidget
    ignoreContext = True
    template = ViewPageTemplateFile('thesaurus_form.pt')

#from .searchform import SearchForm

class DmsThesaurusView(DefaultView):

    def renderForm(self):
        form = DmsThesaurusForm(self.context, self.request)
        #form = SearchForm(self.context, self.request)
        form.update()
        return form.render()


class ListKeywordsView(BrowserView):

    _vocabulary = None
    def get_vocabulary(self):
        context = self
        if self._vocabulary is not None:
            return self._vocabulary
        catalog = getToolByName(context, 'portal_catalog')
        # XXX
        # path = '/'.join(context.getPhysicalPath())
        # print 'path:', path
        results = catalog(portal_type='dmskeyword',
                         ) # path={'query': path,'depth': 1})
        keywords = [x.getObject() for x in results]
        def cmp_keyword(x, y):
            return cmp(x.title.lower(), y.title.lower())
        keywords.sort(cmp_keyword)
        #keyword_ids = [x.id for x in keywords]
        _c = SimpleVocabulary.createTerm
        keyword_terms = [ _c(x.id, x.id, x.title) for x in keywords ]
        self._vocabulary = SimpleVocabulary(keyword_terms)
        return self._vocabulary

    def __call__(self):
        from plone.i18n.normalizer.fr import normalizer
        self.request.response.setHeader('Content-type', 'text/plain')

        query_string = unicode(self.request.form.get('q'), 'utf-8')
        query_terms = [normalizer.normalize(x) for x in query_string.split()]

        startswith = []
        intermediate = []
        other = []
        q = query_string.lower()
        for value in self.get_vocabulary().by_token.values():
            for term in query_terms:
                if not term in value.title.lower():
                    break
            else:
                item = (value.title.lower(), '%s|%s' % (value.title, value.value))
                added = False
                if value.title.lower().startswith(q):
                    startswith.append(item)
                    added = True
                for te in value.title.split():
                    if te.lower().startswith(q):
                        intermediate.append(item)
                        added = True
                        break;
                else:
                    other.append(item)
        startswith.sort()
        intermediate.sort()
        other.sort()
        r = []
        for l in (startswith, intermediate, other):
            for t, e in l:
                r.append(e)
                if len(r) > 29:
                    return '\n'.join(r)
        return '\n'.join(r)
