from datetime import datetime

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.store import (Message as ModelMessage,
                          MessagePart as ModelMessagePart,
                          IndexedMessage,
                          MailIndexMessage)


class MessagePart(AbstractCore):

    _model_class = ModelMessagePart

    text_content_types = ['text/plain', 'text/html']

    @classmethod
    def create(cls, part, users):
        users_id = dict((user.id, 0) for user in users)
        size = len(part.get_payload())
        part = super(MessagePart, cls).\
            create(content_type=part.get_content_type(),
                   size=size,
                   filename=part.get_filename(),
                   payload=part.get_payload(),
                   users=users_id)
        return part

    def get_text(self):
        """Extract text information from part if possible"""
        if self.content_type in self.text_content_types:
            return self.payload
        return None


class Message(AbstractCore):

    _model_class = ModelMessage
    _index_class = IndexedMessage

    @classmethod
    def create_from_mail(cls, user, mail, parts=[], contacts=[]):
        index = MailIndexMessage(mail, parts, contacts)
        parts_id = [x.id for x in parts]
        message_id = user.new_message_id()
        thread_id = user.get_thread_id(index.thread_id)
        msg = cls.create(user_id=user.id,
                         message_id=message_id,
                         thread_id=thread_id,
                         date_insert=datetime.utcnow(),
                         external_message_id=index.message_id,
                         external_thread_id=index.thread_id,
                         parts=parts_id)
        # set message_id into parts
        for part in parts:
            part.users[user.id] = msg.message_id
            part.save()
        # XXX write raw message in store using msg pkey
        # XXX index message asynchronously ?
        cls._index_class.create_index(user.id, message_id, index)
        log.debug('Indexing message %s:%d' % (user.id, message_id))
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
