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


class NoThesaurusFound(Exception):
    """No thesaurus found"""


class ThesaurusKeywordsWidget(SequenceWidget):
    implements(IThesaurusKeywordsWidget)

    def __init__(self, request, display_backrefs=False):
        self.display_backrefs = display_backrefs
        super(ThesaurusKeywordsWidget, self).__init__(request)

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
        thesaurus = self.context

        # XXX attention on remonte a partir d'un document ou d'un kw

        value = []
        for token in self.value:
            # Ignore no value entries. They are in the request only.
            if token == self.noValueToken:
                continue

            term = self.terms.getTermByToken(token)

            value.append(
                {'title': term.title,
                 'href': '#dummy',
                 })
        return value


@adapter(IThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def ThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, ThesaurusKeywordsWidget(
                request, display_backrefs=field.display_backrefs))

