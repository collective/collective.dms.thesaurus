from zope.interface import implementer
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapter

from zope import schema

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form.interfaces import IFormLayer, IFieldWidget, ITextWidget
from z3c.form.widget import FieldWidget
from z3c.form import form, field
from z3c.form.browser import text


from plone.formwidget.autocomplete.widget import AutocompleteSelectionWidget
from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget

from plone.dexterity.browser.view import DefaultView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


from collective.dms.thesaurus import _

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


class DmsThesaurusView(DefaultView):

    def renderForm(self):
        form = DmsThesaurusForm(self.context, self.request)
        form.update()
        return form.render()


class ListKeywordsView(BrowserView):

    _items = None

    def getItems(self):
        context = self.context
        if self._items is not None:
            return self._items
        titles = list()
        self._items = list()

        catalog = getToolByName(context, 'portal_catalog')
        path = '/'.join(context.getPhysicalPath())
        for brain in catalog(portal_type='dmskeyword',
                         path={'query': path,'depth': 1}
                         ) :
            obj = brain.getObject()
            normalized = normalizer.normalize(obj.title).lower()
            if normalized in titles:
                continue
            self._items.append((normalized, obj.title, obj.id))
            titles.append(normalized)
            for equiv in obj.equivs:
                normalized = normalizer.normalize(equiv).lower()
                if normalized in  titles:
                    continue
                self._items.append((normalized, equiv, obj.id))

        def cmp_keyword(x, y):
            return cmp(x[0].lower(), y[0].lower())
        self._items.sort(cmp_keyword)

        return self._items

    def __call__(self):
        self.request.response.setHeader('Content-type', 'text/plain')

        query_string = unicode(self.request.form.get('q'), 'utf-8')
        query_terms = [normalizer.normalize(x) for x in query_string.split()]

        startswith = []
        intermediate = []
        other = []
        q = query_string.lower()
        for normalized, title, id in self.getItems():
            for term in query_terms:
                if not term in title.lower():
                    break
                else:
                    item = '%s|%s' % (title, id)
                    if title.lower().startswith(q):
                        startswith.append((normalized, item))
                        continue
                    for word in title.split():
                        if word.lower().startswith(q):
                            intermediate.append((normalized, item))
                        continue
                    other.append((normalized, item))

        startswith.sort()
        intermediate.sort()
        other.sort()

        result = list()
        for _list in (startswith, intermediate, other):
            for item in _list:
                result.append(item[1])
                if len(result) > 29:
                    return '\n'.join(result)
        return '\n'.join(result)
