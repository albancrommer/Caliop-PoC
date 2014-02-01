from caliop.store import (Contact as ModelContact,
                          ContactLookup as ModelLookup,
                          IndexedContact)
from caliop.core.base import AbstractCore
from caliop.core.user import User


class ContactLookup(AbstractCore):

    _model_class = ModelLookup


class Contact(AbstractCore):

    _model_class = ModelContact
    _index_class = IndexedContact

    @classmethod
    def create(cls, user, infos):
        c = super(Contact, cls).create(user_id=user.id, infos=infos)
        print("Created contact %s" % c.id)
        # Create infos lookup
        for k, v in infos.iteritems():
            if 'tel' in k or 'mail' in k:
                ContactLookup.create(user_id=user.id, value=v, contact_id=c.id)
        # Index contact
        cls._index_class.create(user.id, c.id, infos)
        return cls(c)
