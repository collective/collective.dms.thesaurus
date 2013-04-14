from zope import schema
from zope.interface import implements, implementer
from zope.component import adapter

from zope.schema.interfaces import ISet
from zope.schema.interfaces import IFromUnicode
from z3c.form.interfaces import IFormLayer, IFieldWidget, ISequenceWidget
from z3c.form.widget import FieldWidget, SequenceWidget

from . import _

import utils


class IThesaurusKeywords(ISet):
    pass

class ThesaurusKeywords(schema.Set):
    implements(IThesaurusKeywords, IFromUnicode)

    def __init__(self, display_backrefs=False, **kw):
        self.display_backrefs = display_backrefs
        voc = kw.pop('vocabulary', u'dms.thesaurus.simple')
        vt = kw.pop('value_type', schema.Choice(vocabulary=voc))
        super(ThesaurusKeywords, self).__init__(value_type=vt, **kw)


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
        thesaurus = utils.get_thesaurus_object(self.context)
        if thesaurus is None:
            return ''
        thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
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
        thesaurus = utils.get_thesaurus_object(self.context)
        thesaurus_path = '/'.join(thesaurus.getPhysicalPath())
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

