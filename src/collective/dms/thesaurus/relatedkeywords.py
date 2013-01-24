from zope.interface import implements, implementer
from zope.component import adapter, getUtility
from zope.app.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree.widget import MultiContentTreeWidget
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IRelatedThesaurusKeywords(IRelationList):
    """"""

class RelatedThesaurusKeywordsWidget(MultiContentTreeWidget):
    display_template = ViewPageTemplateFile('related-thesaurus-keywords-display.pt')
    
    def __init__(self, display_backrefs, request):
        self.display_backrefs = display_backrefs
        super(RelatedThesaurusKeywordsWidget, self).__init__(request)

    def get_url(self, v):
        return v

    def get_label(self, v):
        term = self.terms.getTermByToken(v)
        return term.title

    def tuples(self):
        refs = [(self.get_url(x), self.get_label(x)) for x in self.value]
        return refs

@adapter(IRelatedThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def RelatedThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, RelatedThesaurusKeywordsWidget(field.display_backrefs, request))

class RelatedThesaurusKeywords(RelationList):
    implements(IRelatedThesaurusKeywords)

    def __init__(self, **kwargs):
        source_config = dict()
        source_config['portal_type'] = ('dmskeyword',)
        RelationList.__init__(self,
                        value_type=RelationChoice(
                            title=u'',
                            source=ObjPathSourceBinder(**source_config)),
                        **kwargs)

