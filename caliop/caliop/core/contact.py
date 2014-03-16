from datetime import datetime
from caliop.store import (Contact as ModelContact,
                          ContactLookup as ModelLookup,
                          IndexedContact)
from caliop.core.base import AbstractCore


class ContactLookup(AbstractCore):

    _model_class = ModelLookup

    @classmethod
    def get(cls, user, value):
        # XXX : use NotFound
        try:
            obj = cls._model_class.get(user_id=user.id, value=value)
            return cls(obj)
        except:
            return None


class Contact(AbstractCore):

    _model_class = ModelContact
    _index_class = IndexedContact

    @classmethod
    def create(cls, user, infos):
        c = super(Contact, cls).create(user_id=user.id, infos=infos,
                                       date_insert=datetime.utcnow())
        # Create infos lookup
        for k, v in infos.iteritems():
            if 'tel' in k or 'mail' in k:
                ContactLookup.create(user_id=user.id, value=v, contact_id=c.id)
        # Index contact
        cls._index_class.create(user.id, c.id, infos)
        return c

    @classmethod
    def by_id(cls, user, contact_id):
        contact = cls._model_class.get(user_id=user.id, id=contact_id)
        obj = cls(contact)
        return obj.to_api()

    @classmethod
    def list_by_group(cls, user):
        contacts = cls._model_class.objects.filter(user_id=user.id)
        # group them by groups, can repeat same contact so
        groups = {'unknown': []}
        for contact in contacts:
            if contact.groups:
                for group in contact.groups:
                    g = groups.setdefault(group, [])
                    if not contact in g:
                        g.append(cls(contact))
            else:
                if not contact in groups['unknown']:
                    groups['unknown'].append(cls(contact))
        return groups

    def to_api(self):
        return {
            "id": self.id,
            "firstName": self.infos.get('mail'),
            "lastName": self.last_name,
            "avatar": self.infos.get('avatar', 'avatar.png'),
            "date_created": self.date_insert,
        }


class Recipient(object):
    """Store a contact reference and one of it's address used in a message"""

    def __init__(self, contact, address):
        self.contact = contact
        self.address = address
