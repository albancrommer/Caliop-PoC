from datetime import datetime
# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.store import (ThreadLookup as ModelThreadLookup,
                          Thread as ModelThread,
                          IndexedThread)


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
    _index_class = IndexedThread

    @classmethod
    def from_mail(cls, user, mail, contacts, tags):
        # XXX split into create and update methods
        # XXX concurrency will have to be considered correctly
        external_id = mail.get('Thread-ID')
        lookup = None
        if external_id:
            log.debug('Lookup thread %s for %s' % (external_id, user.id))
            lookup = ThreadLookup.get(user, external_id)
        if lookup:
            # Existing thread
            thread = cls.get(user_id=user.id, thread_id=lookup.thread_id)
            log.debug('Get thread %s' % thread.thread_id)
            index = cls._index_class.get(user.id, thread.thread_id)
            if not index:
                log.error('Index not found for thread %s' % thread.thread_id)
                raise Exception
            index_data = {
                'slug': mail.get_payload()[:200],
                'date_update': datetime.utcnow(),
            }
            if contacts:
                index_data.update({'contact': [x.id for x in contacts]})
            if tags:
                index_data.update({'tags': tags})
            index.update(index_data)
            log.debug('Update index for thread %s' % thread.thread_id)
        else:
            # Create new thread
            new_id = user.new_thread_id()
            thread = cls.create(user_id=user.id, thread_id=new_id,
                                date_insert=datetime.utcnow())
            log.debug('Created thread %s' % thread.thread_id)
            index_data = {
                'thread_id': thread.thread_id,
                'date_insert': thread.date_insert,
                'date_update': datetime.utcnow(),
                'slug': mail.get_payload()[:200],
                'contacts': [x.id for x in contacts],
            }
            if tags:
                index_data.update({'tags': tags})
            cls._index_class.create(user.id, thread.thread_id, index_data)
            log.debug('Create index for thread %s' % thread.thread_id)

        return thread

    @classmethod
    def by_user(cls, user, filters=None, sort=None, limit=None):
        """Fetch indexed threads for main view"""
        if not filters:
            filters = {'tags': 'INBOX'}
        return cls._index_class.filter(user.id, filters)
