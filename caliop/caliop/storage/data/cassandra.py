# -*- coding: utf-8 -*-
"""
Caliop storage data interfaces
"""

from __future__ import absolute_import, print_function, unicode_literals

import uuid

from cqlengine import columns
from cqlengine.models import Model
from zope.interface import implementer

from caliop.helpers.config import Configuration

from .interfaces import (IUser, ICounter, ITag, IContact,
                         IContactLookup, IThread, IMessage, IMessagePart,
                         IMessageLookup, IRawMail)


class BaseModel(Model):

    __abstract__ = True
    __keyspace__ = Configuration('global').get('cassandra.keyspace')


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
    subject = columns.Text()
    external_message_id = columns.Text()
    external_parent_id = columns.Text()
    parts = columns.List(columns.UUID)
    tags = columns.List(columns.Text)


@implementer(IMessagePart)
class MessagePart(BaseModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    position = columns.Integer()
    content_type = columns.Text()
    size = columns.Integer()
    filename = columns.Text()
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
