from zope.interface import Interface
from plone.indexer import indexer

#from collective.dms.thesaurus.dmskeyword import IDmsKeyword

class IDmsKeywordIndexer(Interface):
    """Dexterity behavior interface for enabling the dynamic SearchableText
       indexer on Document objecgs."""


@indexer(IDmsKeywordIndexer)
def dmskeyword_searchable_text(obj):
    indexed_fields = []
    title = obj.Title()
    indexed_fields.append(title)
    equivs = obj.get_equivs()
    for equiv in equivs:
        indexed_fields.append(equiv)
    return u' '.join(indexed_fields)
