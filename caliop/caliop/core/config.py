
# XXX a better context management
from cqlengine import connection
from caliop.config import Configuration
from caliop.storage import registry


def includeme(config):
    conf = Configuration('global')
    connection.setup(conf.get('cassandra.hosts', ['127.0.0.1:9160']))

    # XXX get that really configurable
    from caliop.storage.data import cassandra
    registry.register(cassandra.RawMail)
    registry.register(cassandra.User)
    registry.register(cassandra.Contact)
    registry.register(cassandra.ContactLookup)
    registry.register(cassandra.Counter)

    registry.register(cassandra.Message)
    registry.register(cassandra.MessagePart)
    registry.register(cassandra.MessageLookup)
    registry.register(cassandra.Tag)
    registry.register(cassandra.Thread)

    from caliop.storage.index import elasticsearch
    registry.register(elasticsearch.StorageIndex)
    registry.register(elasticsearch.UserIndex)
    registry.register(elasticsearch.IndexedContact)
    registry.register(elasticsearch.IndexedMessage)
    registry.register(elasticsearch.IndexedThread)
