from datetime import datetime
# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.store import (ThreadLookup as ModelThreadLookup,
                          Thread as ModelThread,
                          IndexedThread)

# XXX temporary
import random

TAGS_LABELS = {
    'INBOX': 8,
    'IMPORTANT': 5,
    'SPAM': 6,
    'WORK': 1,
    'PERSONAL': 2,
    'URGENT': 9
}


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
    def from_user_message(cls, message):
        # XXX split into create and update methods
        # XXX concurrency will have to be considered correctly
        external_id = message.external_thread_id
        lookup = None
        if external_id:
            log.debug('Lookup thread %s for %s' %
                      (external_id, message.user.id))
            lookup = ThreadLookup.get(message.user, external_id)
        if lookup:
            # Existing thread
            thread = cls.by_id(message.user, lookup.thread_id)
            log.debug('Get thread %s' % thread.thread_id)
            index = cls._index_class.get(message.user.id, thread.thread_id)
            if not index:
                log.error('Index not found for thread %s' % thread.thread_id)
                raise Exception
            index_data = {
                'slug': message.text[:200],
                'date_update': datetime.utcnow(),
            }
            if message.contacts:
                index_data.update({
                    'contacts': [x.id for x in message.contacts]
                })
            if message.tags:
                index_data.update({'tags': message.tags})
            index.update(index_data)
            log.debug('Update index for thread %s' % thread.thread_id)
        else:
            # Create new thread
            new_id = message.user.new_thread_id()
            thread = cls.create(user_id=message.user.id, thread_id=new_id,
                                date_insert=datetime.utcnow())
            lookup = ThreadLookup.create(user_id=message.user.id,
                                         external_id=external_id,
                                         thread_id=new_id)
            log.debug('Created thread %s' % thread.thread_id)
            index_data = {
                'thread_id': thread.thread_id,
                'date_insert': thread.date_insert,
                'date_update': datetime.utcnow(),
                'slug': message.text[:200],
                'contacts': [x.id for x in message.contacts],
            }
            if message.tags:
                index_data.update({'tags': message.tags})
            cls._index_class.create(message.user.id, thread.thread_id,
                                    index_data)
            log.debug('Create index for thread %s' % thread.thread_id)

        return thread

    @classmethod
    def to_api(self, thread):
        data = {
            'id': thread.thread_id,
            'date_updated': thread.date_update,
            'text': thread.slug,
            'recipients': thread.contacts,
            'labels': [TAGS_LABELS.get(x, 1) for x in thread.tags],
            'security': random.randint(20, 100),
        }
        return data

    @classmethod
    def by_user(cls, user, filters=None, sort=None, limit=None):
        """Fetch indexed threads for main view"""
        if not filters:
            # filters = {'tags': 'INBOX'}
            filters = {'tags': '*'}
        threads = cls._index_class.filter(user.id, filters)
        # XXX : make output compatible for current API
        results = []
        for thr in threads:
            results.append(cls.to_api(thr))
        return results

    @classmethod
    def by_id(cls, user, thread_id):
        thread = cls._index_class.get(user.id, thread_id)
        log.debug('Have thread %r' % thread.to_dict())
        return cls.to_api(thread)
