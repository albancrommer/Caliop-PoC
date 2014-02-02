from datetime import datetime

from caliop.store import (Message as ModelMessage,
                          IndexedMessage,
                          MailIndexMessage)

from caliop.core.base import AbstractCore


class Message(AbstractCore):

    _model_class = ModelMessage
    _index_class = IndexedMessage

    @classmethod
    def create_from_mail(cls, user, mail):
        index = MailIndexMessage(mail)

        message_id = user.new_message_id()
        msg = cls.create(user_id=user.id,
                         message_id=message_id,
                         date_insert=datetime.utcnow(),
                         external_id=index.message_id,
                         thread_id=index.thread_id)
        # XXX : dispatch attachment
        # XXX write raw message in store using msg pkey
        # XXX index message asynchronously ?
        cls._index_class.create_index(user.id, message_id, index)
        return msg

    @classmethod
    def find(cls, user, filters, sort=None):
        """Query index to get messages matching query"""
        messages = cls._index_class.filter(user.id, filters)
        return messages

    @classmethod
    def by_thread_id(cls, user, thread_id, sort=None):
        params = {'thread_id': thread_id}
        return cls._index_class.filter(user.id, params)
