import uuid
from cqlengine import columns
from cqlengine.models import Model


class User(Model):
    id = columns.Text(primary_key=True)
    password = columns.Text(required=True)
    first_name = columns.Text()
    last_name = columns.Text()
    params = columns.Map(columns.Text, columns.Text)


class Counter(Model):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Counter()
    thread_id = columns.Counter()


class Contact(Model):
    user_id = columns.Text(primary_key=True)
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    # Abstract everything in a map
    infos = columns.Map(columns.Text, columns.Text)


class ContactLookup(Model):
    """Lookup any information needed to recognize a user contact"""
    user_id = columns.Text(primary_key=True)
    value = columns.Text(primary_key=True)
    contact_id = columns.UUID()


class ThreadLookup(Model):
    """Reverse index of external thread_id to internal one"""
    user_id = columns.Text(primary_key=True)
    external_id = columns.Text(primary_key=True)
    thread_id = columns.Integer()


class Thread(Model):
    # XXX threading simplest model, not efficient in many ways.
    user_id = columns.Text(primary_key=True)
    thread_id = columns.Integer(primary_key=True)  # counter.thread_id
    date_insert = columns.DateTime()
    date_update = columns.DateTime(index=True)
    slug = columns.Text()
    # map involved contacts with count of presence
    contacts = columns.Map(columns.Text, columns.Integer)
    # map tags to a thread
    tags = columns.Map(columns.Text, columns.Integer)


class Message(Model):
    user_id = columns.Text(primary_key=True)
    message_id = columns.Integer(primary_key=True)  # counter.message_id
    thread_id = columns.Integer()                   # counter.thread_id
    date_insert = columns.DateTime()
    external_message_id = columns.Text()
    external_thread_id = columns.Text()
    parts = columns.List(columns.UUID)


class MessagePart(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    content_type = columns.Text()
    size = columns.Integer()
    filename = columns.Text()
    # base64 encoded payload
    payload = columns.Text()
    # Map user and related message for this part
    users = columns.Map(columns.Text, columns.Integer)


class RRule(Model):
    """Recurrence Rule"""
    user_id = columns.Text(primary_key=True)    # partition key
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    type = columns.Text()
    occurence = columns.Integer(default=1)
    value = columns.Integer()
    events = columns.List(columns.UUID)


class Event(Model):
    user_id = columns.Text(primary_key=True)    # partition key
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    date_start = columns.DateTime()
    end_date = columns.DateTime()
    description = columns.Text()
    rrule_id = columns.UUID()
    latitude = columns.Float()
    longitude = columns.Float()
