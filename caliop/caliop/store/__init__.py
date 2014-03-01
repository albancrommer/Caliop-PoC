from caliop.store.base import MailIndexMessage, UserIndex
from caliop.store.backends.cassandra import (
    User, Counter, Message, MessagePart, Contact, ContactLookup,
    ThreadLookup, Thread, Event, RRule)
from caliop.store.backends.es import IndexedMessage, IndexedContact

# XXX make a backend factory stuff

ALL = [User, Counter, Message, MessagePart,
       Contact, ContactLookup, ThreadLookup,
       Thread, Event, RRule,
       MailIndexMessage, UserIndex,
       IndexedMessage, IndexedContact]
