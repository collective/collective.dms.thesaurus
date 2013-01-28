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

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from .relatedkeywords import RelatedThesaurusKeywords
from .relatedkeywords import RelatedThesaurusKeywordsWidget
from .relatedkeywords import ThesaurusPathSourceBinder

class IBroaderThesaurusKeywords(IRelationList):
    """"""


@adapter(IBroaderThesaurusKeywords, IFormLayer)
@implementer(IFieldWidget)
def BroaderThesaurusKeywordsFieldWidget(field, request):
    return FieldWidget(field, RelatedThesaurusKeywordsWidget(
                                request, from_attribute='broader'))

class BroaderThesaurusKeywords(RelatedThesaurusKeywords):
    implements(IBroaderThesaurusKeywords)

    def __init__(self, **kwargs):
        RelationList.__init__(self,
                        value_type=RelationChoice(
                            title=u'',
                            source=ThesaurusPathSourceBinder()),
                        **kwargs)

