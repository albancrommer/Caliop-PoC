# -*- coding: utf-8 -*-
"""
Caliop user's messages
"""
from __future__ import absolute_import, print_function, unicode_literals

import base64
from datetime import datetime

# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.helpers.log import log

from caliop.storage import registry
from caliop.storage.data.interfaces import (IMessage, IMessagePart,
                                            IMessageLookup)
from caliop.storage.index.interfaces import IIndexedMessage

from .base import BaseCore
from .thread import Thread
from .contact import Contact


class MessagePart(BaseCore):

    _model_class = registry.get(IMessagePart)

    text_content_types = ['text/plain', 'text/html']

    @classmethod
    def create(cls, part, users, position):
        users_id = dict((user.user_id, 0) for user in users)
        size = len(part.get_payload())
        # XXX : decode not here
        charsets = part.get_charsets()
        if len(charsets) != 1:
            raise Exception('Invalid number of charset for part : %r' %
                            charsets)
        payload = part.get_payload()
        if 'Content-Transfer-Encoding' in part.keys() and \
            'text' in part.get('Content-Type'):
            if part.get('Content-Transfer-Encoding') == 'base64':
                payload = base64.b64decode(payload)
        if charsets[0]:
            payload = payload. \
                decode(charsets[0], 'replace'). \
                encode('utf-8')
        if part.get('Content-Disposition'):
            if ';' in part.get('Content-Disposition'):
                disposition, _ = part.get('Content-Disposition').split(';', 2)
            else:
                disposition = part.get('Content-Disposition')
        else:
            disposition = None
        part = super(MessagePart, cls).\
            create(content_type=part.get_content_type(),
                   position=position,
                   size=size,
                   filename=part.get_filename(),
                   disposition=disposition,
                   payload=payload,
                   users=users_id)
        return part

    def get_url(self):
        # XXX not here
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


class MessageLookup(BaseCore):

    _model_class = registry.get(IMessageLookup)

    @classmethod
    def create(cls, message, **kwargs):

        if kwargs['external_message_id']:
            # Create a message lookup
            lookup = kwargs.get('lookup', None)
            offset = lookup.offset + 1 if lookup else 0
            super(MessageLookup, cls).create(user_id=message.user_id,
                                             external_id=message.external_message_id,
                                             message_id=message.message_id,
                                             thread_id=message.thread_id,
                                             offset=offset)
        else:
            log.warn('No message lookup possible for %s' % message.message_id)
            offset = None

    @classmethod
    def get(cls, user_id, external_id):
        try:
            return cls._model_class.get(user_id=user_id,
                                        external_id=external_id)
        except DoesNotExist:
            return None


class Message(BaseCore):

    _model_class = registry.get(IMessage)
    _lookup_classes = {('user_id', 'external_id'): MessageLookup}
    _index_class = registry.get(IIndexedMessage)
    _pkey_name = 'message_id'

    @property
    def offset(self):
        try:
            return MessageLookup.get(self.user_id,
                                     self.external_message_id).offset
        except Exception as exc:  # otherwise we are going in the __getattr__
            log.exception('Exception occured while getting the message lookup')
            return 0

    @classmethod
    def from_user_message(cls, message):
        # Lookup by external_id
        parent_id = message.external_parent_id
        message_id = message.user.new_message_id()
        parts_id = [part.id for part in message.parts]
        lookup = None
        if parent_id:
            log.debug('Lookup message %s for %s' %
                      (parent_id, message.user.user_id))
            lookup = MessageLookup.get(message.user.user_id, parent_id)
        answer_to = lookup.message_id if lookup else None

        # Create or update thread
        thread = Thread.from_user_message(message, lookup)

        indexed_parts = []
        for part in message.parts:
            if not part.can_index():
                continue
            indexed_parts.append({'id': part.id,
                                  'size': part.size,
                                  'content_type': part.content_type,
                                  'filename': part.filename,
                                  'content': part.payload})
        if message.contact_from:
            contact_from = message.contact_from.contact_id
        else:
            contact_from = None
        msg = cls.create(user_id=message.user.user_id,
                         message_id=message_id,
                         thread_id=thread.thread_id,
                         date_insert=datetime.utcnow(),
                         security_level=message.security_level,
                         subject=message.subject,
                         external_message_id=message.external_message_id,
                         external_parent_id=parent_id,
                         parts=parts_id,
                         tags=message.tags,
                         flags=[r'Recent'],
                         lookup=lookup,
                         # Indexed fields
                         _indexed_extra={
                             'from_': contact_from,
                             'headers': message.headers,
                             'text': message.text,
                             'answer_to': answer_to,
                             'contacts': [contact.to_dict()
                                          for contact in message.recipients],
                             'date': message.date,
                             'size': message.size,
                             'parts': indexed_parts
                             },
                         )

        # set message_id into parts
        for part in message.parts:
            part.users[message.user.user_id] = msg.message_id
            part.save()

        return msg

    @classmethod
    def find(cls, user, filters, order=None, limit=None):
        """Query index to get messages matching query"""
        messages = cls._index_class.filter(user.user_id, filters,
                                           order=order, limit=limit)
        return messages

    @classmethod
    def to_api(cls, user, message):
        parts = [MessagePart.get(x['id']) for x in message.parts]
        parts = sorted(parts, key=lambda x: x.position)
        text = "<br />".join([x.get_text() for x in parts])
        from_ = Contact.by_id(user, message.from_)
        data = {
            "id": message.message_id,
            "title": message.subject,
            "body": text,
            "date_sent": message.date,
            "security": message.security_level,
            "author": from_,
            "thread_id": message.thread_id,
            # TOFIX
            "protocole": "email",
            'answer_to': message.answer_to,
            'offset': message.offset,
        }
        return data

    @classmethod
    def by_id(cls, user, message_id):
        msg = cls._index_class.get(user.user_id, message_id)
        return cls.to_api(user, msg)

    @classmethod
    def index_by_id(cls, user_id, message_id):
        # XXX : bad design on by_id methods (all objects) make this
        # necessary, TOREMOVE later
        return cls._index_class.get(user_id, message_id)

    @classmethod
    def by_thread_id(cls, user, thread_id, order=None, limit=None):
        params = {'thread_id': thread_id}
        messages = cls._index_class.filter(user.user_id, params,
                                           order=order, limit=limit)
        results = [cls.to_api(user, x) for x in messages]
        return sorted(results, key=lambda x: x.get('offset', 0))


class BaseMessage(object):
    """Base object to store"""

    def __init__(self, recipients, subject=None, text=None,
                 tags=[], security_level=0, date=None,
                 attachments=[], headers=[],
                 thread_id=None, message_id=None, parent_message_id=None,
                 external_message_id=None
                 ):
        self.recipients = recipients
        self.subject = subject
        self.text = text
        self.tags = tags
        self.security_level = security_level
        self.date = date
        self.parts = attachments
        self.headers = headers
        self.thread_id = thread_id
        self.message_id = message_id
        self.parent_message_id = parent_message_id
        self.external_message_id = external_message_id
        self.size = len(self.text)
