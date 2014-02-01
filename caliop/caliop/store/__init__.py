from caliop.store.base import MailIndexMessage, UserIndex
from caliop.store.backends.cassandra import (
    User, Counter, Message, Contact, ContactLookup,
    Event, RRule)
from caliop.store.backends.es import IndexedMessage

# XXX make a backend factory stuff

ALL = [User, Counter, Message, Contact, ContactLookup, Event, RRule,
       IndexedMessage, MailIndexMessage, UserIndex]
