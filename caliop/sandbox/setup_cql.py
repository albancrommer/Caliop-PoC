#!/usr/bin/env python

"""
This script create cassandra models in a local cassandra instance
"""
from cqlengine import connection
from cqlengine.management import sync_table

from caliop.config import Configuration
Configuration.load('./conf.yaml', 'global')
from caliop.store import (User, Message, Counter, Contact,
                          ContactLookup, MessagePart, MessageLookup,
                          Thread)

connection.setup(['127.0.0.1:9160'])

sync_table(User)
sync_table(Message)
sync_table(MessagePart)
sync_table(MessageLookup)
sync_table(Counter)
sync_table(Contact)
sync_table(ContactLookup)
sync_table(Thread)
