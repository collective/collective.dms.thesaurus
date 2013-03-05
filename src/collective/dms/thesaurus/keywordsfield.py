from Acquisition import aq_parent

from zope import schema
from zope.interface import implements, implementer
from zope.component import adapter

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.schema.interfaces import ISet
from zope.schema.interfaces import IFromUnicode
from z3c.form.interfaces import IFormLayer, IFieldWidget, ISequenceWidget
#from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget, SequenceWidget
#from z3c.form.widget import Widget
#from z3c.form.browser.select import SelectWidget

from . import _

class IThesaurusKeywords(ISet):
    pass

class ThesaurusKeywords(schema.Set):
    implements(IThesaurusKeywords, IFromUnicode)

    def __init__(self, display_backrefs=False, **kw):
        self.display_backrefs = display_backrefs
        vocabulary = kw.pop('vocabulary', u'dms.thesaurus.global')
        super(ThesaurusKeywords, self).__init__(
                    value_type=schema.Choice(vocabulary=vocabulary),
                    **kw)


class IThesaurusKeywordsWidget(ISequenceWidget):
    pass




JS_TEMPLATE = """
$(document).ready(function() {
  $('a.kw_add_link').prepOverlay({
    subtype: 'ajax',
    filter: '#content>*',
    urlmatch: '.*',
    urlreplace: '%(thesaurus_url)s'
  });
});
"""

class ThesaurusKeywordsWidget(SequenceWidget):
    implements(IThesaurusKeywordsWidget)

    def __init__(self, request, display_backrefs=False):
        self.display_backrefs = display_backrefs
        super(ThesaurusKeywordsWidget, self).__init__(request)

    @property
    def js(self):
        thesaurus_path = '/'.join(self.context.thesaurusPath())
        return JS_TEMPLATE % dict(
            thesaurus_url=thesaurus_path
            )

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
        thesaurus_path = '/'.join(self.context.thesaurusPath())
        value = []
        for token in self.value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue
            term = self.terms.getTermByToken(token)
            value.append(
                {'title': term.title,
                 'href': thesaurus_path + '/' + term.value,
                 })
        return value



@adapter(IThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def ThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, ThesaurusKeywordsWidget(
                request, display_backrefs=field.display_backrefs))

