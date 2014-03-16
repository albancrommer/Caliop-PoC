from datetime import datetime
# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.core.contact import Contact
from caliop.store import Thread as ModelThread, IndexedThread

# XXX temporary
import random


class Thread(AbstractCore):

    _model_class = ModelThread
    _index_class = IndexedThread

    @classmethod
    def get(cls, user, thread_id):
        try:
            return cls._model_class.get(user_id=user.id,
                                        thread_id=thread_id)
        except DoesNotExist:
            return None

    @classmethod
    def from_user_message(cls, message, lookup=None):
        # XXX split into create and update methods
        # XXX concurrency will have to be considered correctly
        if lookup:
            # Existing thread
            thread = cls.get(message.user, lookup.thread_id)
            log.debug('Get thread %s' % lookup.thread_id)
            index = cls._index_class.get(message.user.id, lookup.thread_id)
            if not index:
                log.error('Index not found for thread %s' % lookup.thread_id)
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
            log.debug('Update index for thread %s' % lookup.thread_id)
        else:
            # Create new thread
            new_id = message.user.new_thread_id()
            thread = cls.create(user_id=message.user.id, thread_id=new_id,
                                date_insert=datetime.utcnow())
            log.debug('Created thread %s' % thread.thread_id)
            index_data = {
                'thread_id': thread.thread_id,
                'date_insert': thread.date_insert,
                'date_update': datetime.utcnow(),
                'slug': message.text[:200],
                'contacts': [x.contact_id for x in message.contacts],
            }
            if message.tags:
                index_data.update({'tags': message.tags})
            cls._index_class.create(message.user.id, thread.thread_id,
                                    index_data)
            log.debug('Create index for thread %s' % thread.thread_id)

        return thread

    @classmethod
    def expand_contacts(self, user, contacts):
        results = []
        for contact in contacts:
            results.append(Contact.by_id(user, contact))
        return results

    @classmethod
    def expand_tags(self, user, tags):
        user_tags = dict((x.label, x) for x in user.tags)
        results = []
        for tag in tags:
            if tag in user_tags:
                results.append(user_tags[tag])
            else:
                log.warn('Unknow user tag %r' % tag)
        return results

    @classmethod
    def to_api(self, thread, recipients, tags):
        data = {
            'id': thread.thread_id,
            'date_updated': thread.date_update,
            'text': thread.slug,
            'recipients': recipients,
            'labels': [x.to_api() for x in tags],
            'security': random.randint(20, 100),
        }
        return data

    @classmethod
    def by_user(cls, user, filters=None, order=None, limit=None):
        """Fetch indexed threads for main view"""
        if not filters:
            # filters = {'tags': 'INBOX'}
            filters = {'tags': '*'}
        threads = cls._index_class.filter(user.id, filters,
                                          order=order, limit=limit)
        # XXX : make output compatible for current API
        results = []
        for thr in threads:
            recipients = cls.expand_contacts(user, thr.contacts)
            tags = cls.expand_tags(user, thr.tags)
            results.append(cls.to_api(thr, recipients, tags))
        return results

    @classmethod
    def by_id(cls, user, thread_id):
        thread = cls._index_class.get(user.id, thread_id)
        recipients = cls.expand_contacts(user, thread.contacts)
        tags = cls.expand_tags(user, thread.tags)
        return cls.to_api(thread, recipients, tags)
