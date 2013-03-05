from zope.interface import implements, implementer
from zope.component import adapter
#, getUtility

from zope import schema
from zope.schema.interfaces import IList
#from zope.app.intid.interfaces import IIntIds

#from zc.relation.interfaces import ICatalog

from z3c.form.interfaces import IFormLayer, IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.multi import MultiWidget

#from z3c.relationfield.interfaces import IRelationList
#from z3c.relationfield.schema import RelationChoice, RelationList

#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IThesaurusKeywordEquivalences(IList):
    """"""

class ThesaurusKeywordEquivalences(schema.List):
    implements(IThesaurusKeywordEquivalences)

    def __init__(self, **kwargs):
        super(ThesaurusKeywordEquivalences, self).__init__(
                        value_type=schema.TextLine(
                            title=u'', required=False),
                        **kwargs)


class ThesaurusKeywordEquivalencesWidget(MultiWidget):

    def __init__(self, request):
        super(ThesaurusKeywordEquivalencesWidget, self).__init__(request)

    def terms(self):
        return self.value


@adapter(IThesaurusKeywordEquivalences, IFormLayer)
@implementer(IFieldWidget)
def ThesaurusKeywordEquivalencesFieldWidget(field, request):
    return FieldWidget(field, ThesaurusKeywordEquivalencesWidget(request))

