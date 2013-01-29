import json

from zope import component
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from Products.Five.browser import BrowserView

from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent, ObjectModifiedEvent


class ImportJson(BrowserView):
    def __call__(self):
        self.intids = component.getUtility(IIntIds)

        path = '/tmp/thesaurus.json'
        # XXX: replace with a path given in the query string, or load json
        # from POST data

        terms = json.load(file(path))
        term_intids = {}

        # 1st step; create object for terms
        for term_id, term in terms.items():
            try:
                object = getattr(self.context, term_id)
            except AttributeError:
                self.context.invokeFactory('dmskeyword', term_id,
                                   title=term.get('title'))
                object = getattr(self.context, term_id)
                notify(ObjectAddedEvent(object))
                try:
                    term_intids[term_id] = self.intids.getId(object)
                except KeyError:
                    self.intids.register(object)
            object.title = term.get('title')
            object.historical_note = term.get('historical_note')
            object.scope_note = term.get('scope_note')
            object.equivs = term.get('equivalents')
            term_intids[term_id] = self.intids.getId(object)

        # 2nd step; add relations
        for term_id, term in terms.items():
            object = getattr(self.context, term_id)
            object.related = [RelationValue(term_intids[x]) for x in term.get('related', [])]
            object.broader = [RelationValue(term_intids[x]) for x in term.get('parents', [])]
            notify(ObjectModifiedEvent(object))

        return 'OK'
