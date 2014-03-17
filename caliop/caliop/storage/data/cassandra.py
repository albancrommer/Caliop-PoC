import uuid
from cqlengine import columns
from cqlengine.models import Model

from caliop.helpers.config import Configuration


class BaseModel(Model):

    __abstract__ = True
    __keyspace__ = Configuration('global').get('cassandra.keyspace')


class User(BaseModel):
    id = columns.Text(primary_key=True)
    password = columns.Text(required=True)
    date_insert = columns.DateTime()
    first_name = columns.Text()
    last_name = columns.Text()
    params = columns.Map(columns.Text, columns.Text)


class Counter(BaseModel):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Counter()
    thread_id = columns.Counter()


class Tag(BaseModel):
    user_id = columns.Text(primary_key=True)
    label = columns.Text(primary_key=True)
    background = columns.Text()
    color = columns.Text()


class Contact(BaseModel):
    user_id = columns.Text(primary_key=True)
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    first_name = columns.Text()
    last_name = columns.Text()
    date_insert = columns.DateTime()
    date_update = columns.DateTime()
    groups = columns.List(columns.Text)
    # Abstract everything else in a map
    infos = columns.Map(columns.Text, columns.Text)


class ContactLookup(BaseModel):
    """Lookup any information needed to recognize a user contact"""
    user_id = columns.Text(primary_key=True)
    value = columns.Text(primary_key=True)
    contact_id = columns.UUID()


class Thread(BaseModel):
    # XXX threading simplest model, most data are only in index
    user_id = columns.Text(primary_key=True)
    thread_id = columns.Integer(primary_key=True)  # counter.thread_id
    date_insert = columns.DateTime()
    security_level = columns.Integer()


class Message(BaseModel):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Integer(primary_key=True)  # counter.message_id
    thread_id = columns.Integer()                   # counter.thread_id
    date_insert = columns.DateTime()
    security_level = columns.Integer()
    external_message_id = columns.Text()
    external_parent_id = columns.Text()
    parts = columns.List(columns.UUID)
    tags = columns.List(columns.Text)


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


class MessageLookup(BaseModel):
    """Reverse index for external message id"""
    user_id = columns.Text(primary_key=True)
    external_id = columns.Text(primary_key=True)
    message_id = columns.Integer()
    thread_id = columns.Integer()
    offset = columns.Integer()


class RRule(BaseModel):
    """Recurrence Rule"""
    user_id = columns.Text(primary_key=True)    # partition key
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    type = columns.Text()
    occurence = columns.Integer(default=1)
    value = columns.Integer()
    events = columns.List(columns.UUID)


class Event(BaseModel):
    user_id = columns.Text(primary_key=True)    # partition key
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    date_start = columns.DateTime()
    end_date = columns.DateTime()
    description = columns.Text()
    rrule_id = columns.UUID()
    latitude = columns.Float()
    longitude = columns.Float()
