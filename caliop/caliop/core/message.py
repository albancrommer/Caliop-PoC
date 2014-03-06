from datetime import datetime

# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log
from caliop.core.base import AbstractCore
from caliop.core.thread import Thread
from caliop.store import (Message as ModelMessage,
                          MessagePart as ModelMessagePart,
                          MessageLookup as ModelMessageLookup,
                          IndexedMessage,
                          MailIndexMessage)


class MessagePart(AbstractCore):

    _model_class = ModelMessagePart

    text_content_types = ['text/plain', 'text/html']

    @classmethod
    def create(cls, part, users, position):
        users_id = dict((user.id, 0) for user in users)
        size = len(part.get_payload())
        # XXX : decode not here
        charsets = part.get_charsets()
        if len(charsets) != 1:
            raise Exception('Invalid number of charset for part : %r' %
                            charsets)
        if charsets[0] and charsets[0] != 'utf-8':
            payload = part.get_payload().decode(charsets[0]).encode('utf-8')
        else:
            payload = part.get_payload()
        part = super(MessagePart, cls).\
            create(content_type=part.get_content_type(),
                   position=position,
                   size=size,
                   filename=part.get_filename(),
                   payload=payload,
                   users=users_id)
        return part

    def get_url(self):
        return '/parts/%s' % self.id

    def get_text(self):
        """Extract text information from part if possible"""
        if self.content_type == 'text/plain':
            return '<pre>%s</pre>' % self.payload
        if self.content_type == 'text/html':
            return self.payload
        else:
            return '<a href="%s">%s</a>' % (self.get_url(), self.filename)

    def can_index(self):
        return True if self.content_type in self.text_content_types else False


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
    def from_user_message(cls, message):
        # Lookup by external_id
        external_id = message.external_thread_id
        message_id = message.user.new_message_id()
        parts_id = [x.id for x in message.parts]
        lookup = None
        if external_id:
            log.debug('Lookup message %s for %s' %
                      (external_id, message.user.id))
            lookup = MessageLookup.get(message.user, external_id)
        answer_to = lookup.message_id if lookup else None

        # Create or update thread
        thread = Thread.from_user_message(message, lookup)

        msg = cls.create(user_id=message.user.id,
                         message_id=message_id,
                         thread_id=thread.thread_id,
                         date_insert=datetime.utcnow(),
                         external_message_id=message.external_message_id,
                         external_thread_id=message.external_thread_id,
                         parts=parts_id,
                         tags=message.tags)

        # Create a message lookup
        if message.external_message_id:
            offset = lookup.offset + 1 if lookup else 0
            MessageLookup.create(user_id=message.user.id,
                                 external_id=message.external_message_id,
                                 message_id=message_id,
                                 thread_id=thread.thread_id,
                                 offset=offset)
        else:
            log.warn('No message lookup possible for %s' % message_id)
            offset = None
        # set message_id into parts
        for part in message.parts:
            part.users[message.user.id] = msg.message_id
            part.save()
        # XXX write raw message in store using msg pkey
        # XXX index message asynchronously ?
        index = MailIndexMessage(message, thread.thread_id, message_id,
                                 answer_to, offset)
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
        parts = []
        for part in message.parts:
            parts.append(MessagePart.get(part['id']))
        text = "<br />".join([x.get_text() for x in parts])
        data = {
            "id": message.message_id,
            "title": message.subject,
            "body": text,
            "date_sent": message.date,
            "security": message.security_level,
            # "author": message.from_,
            "thread_id": message.thread_id,
            # TOFIX
            "protocole": "email",
            'answer_to': message.answer_to,
            'offset': message.offset,
        }
        return data

    @classmethod
    def by_thread_id(cls, user, thread_id, sort=None):
        params = {'thread_id': thread_id}
        messages = cls._index_class.filter(user.id, params)
        results = [cls.to_api(x) for x in messages]
        return sorted(results, key=lambda x: x.get('offset', 0))
