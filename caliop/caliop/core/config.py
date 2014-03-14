
# XXX a better context management
from cqlengine import connection
from caliop.config import Configuration


def includeme(config):
    conf = Configuration('global')
    connection.setup(conf.get('cassandra.hosts', ['127.0.0.1:9160']))
