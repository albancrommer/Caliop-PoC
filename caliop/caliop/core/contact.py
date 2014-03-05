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
        contact = cls._index_class.get(user.id, contact_id)
        return cls.to_api(contact)

    def to_api(self):
        return {
            "id": self.contact_id,
            "firstName": self.fist_name,
            "lastName": self.last_name,
            "avatar": self.infos.get('avatar'),
            "date_created": self.date_insert,
        }
