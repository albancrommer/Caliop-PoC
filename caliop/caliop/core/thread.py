from datetime import datetime
# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.store import (ThreadLookup as ModelThreadLookup,
                          Thread as ModelThread)


class ThreadLookup(AbstractCore):

    _model_class = ModelThreadLookup

    @classmethod
    def get(cls, user, external_id):
        try:
            return cls._model_class.get(user_id=user.id,
                                        external_id=external_id)
        except DoesNotExist:
            return None


class Thread(AbstractCore):

    _model_class = ModelThread

    @classmethod
    def from_mail(cls, user, mail, contacts, tags):
        external_id = mail.get('Thread-ID')
        lookup = None
        if external_id:
            log.debug('Lookup thread %s for %s' % (external_id, user.id))
            lookup = ThreadLookup.get(user, external_id)
        if lookup:
            # Existing thread
            thread = cls.get(user_id=user.id, thread_id=lookup.thread_id)
            log.debug('Get thread %s' % thread.thread_id)
        else:
            new_id = user.new_thread_id()
            thread = cls.create(user_id=user.id, thread_id=new_id,
                                date_insert=datetime.utcnow())
            log.debug('Created thread %s' % thread.thread_id)
        # Set attributes on thread
        # XXX : bad design
        # XXX : core model do not handle setter on column
        thread.model.slug = mail.get_payload()[:200]
        for contact in contacts:
            if not contact.id in thread.model.contacts:
                current = 0
            else:
                current = thread.model.contacts[contact.id]
            thread.model.contacts[contact.id] = current + 1
        for tag in tags:
            if not tag in thread.model.tags:
                current = 0
            else:
                current = thread.model.tags[tag]
            thread.model.tags[tag] = current + 1

        thread.model.date_update = datetime.utcnow()
        thread.save()
        return thread
