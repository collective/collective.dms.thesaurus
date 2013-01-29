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
    if not isinstance(title, unicode):
        # Title() is a CMF-style accessor, it will therefore a return a
        # utf8-encoded bytestring; encode it back as an unicode string.
        title = unicode(title, 'utf-8')
    indexed_fields.append(title)
#    equivs = obj.get_equivs()
#    for equiv in equivs:
#        if isinstance(title, unicode):
#            equiv = title.encode('utf-8')
#        indexed_fields.append(equiv)
    return u' '.join(indexed_fields)
