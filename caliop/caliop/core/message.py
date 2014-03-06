from datetime import datetime

# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.store import (Message as ModelMessage,
                          MessagePart as ModelMessagePart,
                          MessageLookup as ModelMessageLookup,
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


class MessageLookup(AbstractCore):

    _model_class = ModelMessageLookup

    @classmethod
    def get(cls, user, external_id):
        try:
            return cls._model_class.get(user_id=user.id,
                                        external_id=external_id)
        except DoesNotExist:
            return None


class Message(AbstractCore):

    _model_class = ModelMessage
    _index_class = IndexedMessage

    @classmethod
    def from_user_message(cls, message, thread_id):
        parts_id = [x.id for x in message.parts]
        message_id = message.user.new_message_id()
        msg = cls.create(user_id=message.user.id,
                         message_id=message_id,
                         thread_id=thread_id,
                         date_insert=datetime.utcnow(),
                         external_message_id=message.external_message_id,
                         external_thread_id=message.external_thread_id,
                         parts=parts_id,
                         tags=message.tags)
        if message.external_message_id:
            # Create message lookup
            MessageLookup.create(user_id=message.user.id,
                                 external_id=message.external_message_id,
                                 message_id=message_id,
                                 thread_id=thread_id)

        # set message_id into parts
        for part in message.parts:
            part.users[message.user.id] = msg.message_id
            part.save()
        # XXX write raw message in store using msg pkey
        # XXX index message asynchronously ?
        index = MailIndexMessage(message, thread_id, message_id)
        cls._index_class.create_index(message.user.id, message_id, index)
        log.debug('Indexing message %s:%d' % (message.user.id, message_id))
        return msg

    @classmethod
    def find(cls, user, filters, sort=None):
        """Query index to get messages matching query"""
        messages = cls._index_class.filter(user.id, filters)
        return messages

    @classmethod
    def to_api(cls, message):
        data = {
            "id": message.message_id,
            "title": message.subject,
            "body": message.text,
            "date_sent": message.date,
            "security": message.security_level,
            "author": message.from_,
            "thread_id": message.thread_id,
            # TOFIX
            "protocole": "email",
            'answer_to': 0,
            'offset': 1,
        }
        return data

    @classmethod
    def by_thread_id(cls, user, thread_id, sort=None):
        params = {'thread_id': thread_id}
        messages = cls._index_class.filter(user.id, params)
        return [cls.to_api(x) for x in messages]
