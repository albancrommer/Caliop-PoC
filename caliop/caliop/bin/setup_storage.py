#!/usr/bin/env python
"""
This script create cassandra models in a local cassandra instance.

This should be abstracted in a backend to get many backend supported.
"""
from cqlengine import connection
from cqlengine.management import sync_table

def setup_storage():
    from caliop.store import (User, Message, Counter, Contact,
                              ContactLookup, MessagePart, MessageLookup,
                              Thread)

    sync_table(User)
    sync_table(Message)
    sync_table(MessagePart)
    sync_table(MessageLookup)
    sync_table(Counter)
    sync_table(Contact)
    sync_table(ContactLookup)
    sync_table(Thread)
