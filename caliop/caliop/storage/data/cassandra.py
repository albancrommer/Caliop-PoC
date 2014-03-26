# -*- coding: utf-8 -*-
"""
Caliop storage data interfaces
"""

from __future__ import absolute_import, print_function, unicode_literals

import uuid

from cqlengine import connection, columns
from cqlengine.management import sync_table
from cqlengine.models import Model
from zope.interface import implementer

from caliop.config import Configuration

from .interfaces import (IStorage, IUser, ICounter, ITag, IContact,
                         IContactLookup, IThread, IMessage, IMessagePart,
                         IMessageLookup, IRawMail)


@implementer(IStorage)
class Storage(object):
    """ Data storage """

    @classmethod
    def initialize_db(cls, settings):
        """
        Create the schema
        """
        cls.connect(settings)
        sync_table(User)
        sync_table(Tag)
        sync_table(Message)
        sync_table(MessagePart)
        sync_table(MessageLookup)
        sync_table(Counter)
        sync_table(Contact)
        sync_table(ContactLookup)
        sync_table(Thread)
        sync_table(RawMail)

    @classmethod
    def connect(cls, settings):
        """ Bind the connection to the cassandra. """
        conf = Configuration('global')
        connection.setup(conf.get('cassandra.hosts', ['127.0.0.1:9160']))

    @classmethod
    def disconnect(cls):
        """ Should disconnect but not implemented yet """

    @classmethod
    def get_connection(cls):
        """ do nothing """


class BaseModel(Model):

    __abstract__ = True
    __keyspace__ = Configuration('global').get('cassandra.keyspace')

    @classmethod
    def create(cls, **kwargs):
        kwargs = {key: val for key, val in kwargs.items()
                  if key in cls._columns}
        return super(BaseModel, cls).create(**kwargs)


@implementer(IRawMail)
class RawMail(BaseModel):
    raw_id = columns.Text(primary_key=True)
    users = columns.List(columns.Text)
    data = columns.Bytes()


@implementer(IUser)
class User(BaseModel):
    user_id = columns.Text(primary_key=True)
    password = columns.Text(required=True)
    date_insert = columns.DateTime()
    first_name = columns.Text()
    last_name = columns.Text()
    params = columns.Map(columns.Text, columns.Text)


@implementer(ICounter)
class Counter(BaseModel):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Counter()
    thread_id = columns.Counter()


@implementer(ITag)
class Tag(BaseModel):
    user_id = columns.Text(primary_key=True)
    label = columns.Text(primary_key=True)
    background = columns.Text()
    color = columns.Text()


@implementer(IContact)
class Contact(BaseModel):
    contact_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.Text(primary_key=True)
    first_name = columns.Text()
    last_name = columns.Text()
    date_insert = columns.DateTime()
    date_update = columns.DateTime()
    groups = columns.List(columns.Text)
    # Abstract everything else in a map
    infos = columns.Map(columns.Text, columns.Text)


@implementer(IContactLookup)
class ContactLookup(BaseModel):
    """Lookup any information needed to recognize a user contact"""
    user_id = columns.Text(primary_key=True)
    value = columns.Text(primary_key=True)
    contact_id = columns.UUID()


@implementer(IThread)
class Thread(BaseModel):
    # XXX threading simplest model, most data are only in index
    user_id = columns.Text(primary_key=True)
    thread_id = columns.Integer(primary_key=True)  # counter.thread_id
    date_insert = columns.DateTime()
    security_level = columns.Integer()
    subject = columns.Text()


@implementer(IMessage)
class Message(BaseModel):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Integer(primary_key=True)  # counter.message_id
    thread_id = columns.Integer()                   # counter.thread_id
    date_insert = columns.DateTime()
    security_level = columns.Integer()
    subject = columns.Text()  # Subject of email, the message for short
    external_message_id = columns.Text()
    external_parent_id = columns.Text()
    parts = columns.List(columns.UUID)
    tags = columns.List(columns.Text)
    flags = columns.List(columns.Text)  # Seen, Recent, Deleted, ... IMAP?


@implementer(IMessagePart)
class MessagePart(BaseModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    position = columns.Integer()
    content_type = columns.Text()
    size = columns.Integer()
    filename = columns.Text()
    disposition = columns.Text()
    # base64 encoded payload
    payload = columns.Text()
    # Map user and related message for this part
    users = columns.Map(columns.Text, columns.Integer)


@implementer(IMessageLookup)
class MessageLookup(BaseModel):
    """Reverse index for external message id"""
    user_id = columns.Text(primary_key=True)
    external_id = columns.Text(primary_key=True)
    message_id = columns.Integer()
    thread_id = columns.Integer()
    offset = columns.Integer()


# Calendar

class RRule(BaseModel):
    """Recurrence Rule"""
    user_id = columns.Text(primary_key=True)    # partition key
    rrule_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    type = columns.Text()
    occurrence = columns.Integer(default=1)
    value = columns.Integer()
    events = columns.List(columns.UUID)


class Event(BaseModel):
    user_id = columns.Text(primary_key=True)    # partition key
    event_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    date_start = columns.DateTime()
    end_date = columns.DateTime()
    description = columns.Text()
    rrule_id = columns.UUID()
    latitude = columns.Float()
    longitude = columns.Float()
