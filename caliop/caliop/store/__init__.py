from caliop.store.base import MailIndexMessage, UserIndex
from caliop.store.backends.cassandra import (
    User, Counter, Message, MessagePart, MessageLookup,
    Contact, ContactLookup,
    Thread, Event, RRule)
from caliop.store.backends.es import (IndexedMessage, IndexedContact,
                                      IndexedThread)

# XXX make a backend factory stuff

ALL = [User, Counter, Message, MessagePart, MessageLookup,
       Contact, ContactLookup,
       Thread, Event, RRule,
       MailIndexMessage, UserIndex,
       IndexedMessage, IndexedContact, IndexedThread]
