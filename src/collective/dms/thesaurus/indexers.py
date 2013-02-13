from five import grok
from zope.interface import Interface
from plone.indexer import indexer


class IDmsKeywordIndexer(Interface):
    """Dexterity behavior interface for enabling the dynamic SearchableText
       indexer on Document objects."""


@indexer(IDmsKeywordIndexer)
def dmskeyword_searchable_text(obj):
    indexed_fields = []
    title = unicode(obj.Title(), 'utf-8')
    indexed_fields.append(title)
    if obj.equivs:
        indexed_fields.extend(obj.equivs)
    return u' '.join(indexed_fields)

grok.global_adapter(dmskeyword_searchable_text, name='SearchableText')
