from zope.interface import implements, implementer
from zope.component import adapter, getUtility
from zope.app.intid.interfaces import IIntIds

from zc.relation.interfaces import ICatalog

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree.widget import MultiContentTreeWidget
from plone.formwidget.contenttree.utils import closest_content
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IRelatedThesaurusKeywords(IRelationList):
    """"""

class RelatedThesaurusKeywordsWidget(MultiContentTreeWidget):
    display_template = ViewPageTemplateFile('related-thesaurus-keywords-display.pt')
    
    def __init__(self, request, from_attribute='related', display_backrefs=False):
        self.from_attribute = from_attribute
        self.display_backrefs = display_backrefs
        super(RelatedThesaurusKeywordsWidget, self).__init__(request)

    def get_url(self, v):
        return v

    def get_term(self, v):
        return self.terms.getTermByToken(v)

    def get_label(self, v):
        return self.get_term(v).title

    def get_hn(self, v):
        return self.get_term(v).value.historical_note

    def get_sn(self, v):
        return self.get_term(v).value.scope_note

    def dictvalues(self):
        refs = [dict(
            url=self.get_url(x),
            label=self.get_label(x),
            hn=self.get_hn(x),
            sn=self.get_sn(x),
            ) for x in self.value]
        if self.display_backrefs:
            intids = getUtility(IIntIds)
            catalog = getUtility(ICatalog)
            try:
                doc_intid = intids.getId(self.context)
            except KeyError:
                pass
            else:
                for ref in catalog.findRelations(
                        {'to_id': doc_intid,
                         'from_attribute': self.from_attribute}):
                    tp = dict(
                        url=ref.from_path,
                        label=ref.from_object.Title(),
                        hn=ref.from_object.historical_note,
                        sn=ref.from_object.scope_note
                        )
                    if tp not in refs:
                        refs.append(tp)
        return refs


@adapter(IRelatedThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def RelatedThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, RelatedThesaurusKeywordsWidget(
                request, display_backrefs=field.display_backrefs))

class ThesaurusPathSourceBinder(ObjPathSourceBinder):

    def __call__(self, context):
        selectable_filter = self.selectable_filter
        selectable_filter.criteria['portal_type'] = ('dmskeyword',)
        thesaurus_path = {'query': '/'.join(context.getPhysicalPath()[:-1])}
        selectable_filter.criteria['path'] = thesaurus_path
        return self.path_source(
            closest_content(context),
            selectable_filter=selectable_filter,
            navigation_tree_query=self.navigation_tree_query)


class RelatedThesaurusKeywords(RelationList):
    implements(IRelatedThesaurusKeywords)

    def __init__(self, display_backrefs=False, **kwargs):
        self.display_backrefs = display_backrefs
        RelationList.__init__(self,
                        value_type=RelationChoice(
                            title=u'',
                            source=ThesaurusPathSourceBinder()),
                        **kwargs)

