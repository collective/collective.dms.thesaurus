from zope.interface import implements, implementer
from zope.component import adapter

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree.widget import MultiContentTreeWidget
from plone.formwidget.contenttree.utils import closest_content
from plone.formwidget.contenttree import ObjPathSourceBinder

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IThesaurusKeywords(IRelationList):
    """"""

class ThesaurusKeywordsWidget(MultiContentTreeWidget):
    display_template = ViewPageTemplateFile('thesaurus-keywords-display.pt')

    def __init__(self, request):
        super(ThesaurusKeywordsWidget, self).__init__(request)

    def terms(self):
        return [ x for x in self.value ]


@adapter(IThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def ThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, ThesaurusKeywordsWidget(request))

class ThesaurusPathSourceBinder(ObjPathSourceBinder):

    def __call__(self, context):
        selectable_filter = self.selectable_filter
        selectable_filter.criteria['portal_type'] = ('dmskeyword',)
        #thesaurus_path = {'query': '/'.join(context.getPhysicalPath()[:-1])}
        #selectable_filter.criteria['path'] = thesaurus_path
        return self.path_source(
            closest_content(context),
            selectable_filter=selectable_filter,
            navigation_tree_query=self.navigation_tree_query)


class ThesaurusKeywords(RelationList):
    implements(IThesaurusKeywords)

    def __init__(self, **kwargs):
        RelationList.__init__(self,
                        value_type=RelationChoice(
                            title=u'',
                            source=ThesaurusPathSourceBinder()),
                        **kwargs)

