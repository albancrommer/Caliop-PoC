from datetime import datetime

import requests
from zope.interface import implementer

from caliop.config import Configuration
from caliop.helpers.json import to_json
from .interfaces import (IStorageIndex,
                         IMailIndexMessage, IUserIndex, IIndexedMessage,
                         IIndexedContact, IIndexedThread)
from ..registry import get_component


@implementer(IStorageIndex)
class StorageIndex(object):
    def initialize_db(cls, settings):
        """ Do nothing """

    def connect(cls, settings):
        """ Do nothing """

    def disconnect(cls):
        """ Do nothing """

    def get_connection(cls):
        return Configuration('global').get('index_server.url')


@implementer(IUserIndex)
class UserIndex(object):
    """Only here to manage user index globally (create, delete)"""

    @classmethod
    def create(cls, user):
        # Create index for user
        index_server_url = get_component(IStorageIndex).get_connection()
        route = '%s/%s' % (index_server_url, user.user_id)
        res = requests.put(route)
        return True if res.status_code == 200 else False


class BaseIndexDocument(object):
    """Base class for indexed objects"""

    columns = []
    type = None

    def __init__(self, data):
        # XXX : tofix, need to handle better ES result
        if '_source' in data:
            data = data['_source']
        for col in self.columns:
            setattr(self, col, data.get(col, None))

    @classmethod
    def get(cls, user_id, uid):
        index_server_url = get_component(IStorageIndex).get_connection()
        route = "%s/%s/%s/%s" % (index_server_url, user_id, cls.type, uid)
        res = requests.get(route)
        if res.status_code == 200:
            data = res.json()
            obj = cls(data['_source']) if data['_source'] else None
            # XXX : design problem, we should not do this
            setattr(obj, 'user_id', user_id)
            setattr(obj, 'uid', uid)
            return obj
        raise Exception('Index %s/%s/%s not found' % (user_id, cls.type, uid))

    def refresh(self):
        self.get(self.user_id, self.uid)

    def update(self, query):
        # XXX surely not secure
        route = "%s/%s/%s/%s/_update" % \
            (self.index_server_url, self.user_id, self.type, self.uid)
        res = requests.post(route, data=to_json(query))
        return True if res.status_code == 200 else False

    @classmethod
    def create(cls, user_id, id, data):
        index_server_url = get_component(IStorageIndex).get_connection()
        route = '%s/%s/%s/%s' % (index_server_url, user_id, cls.type, id)
        res = requests.put(route, to_json(data))
        return True if res.status_code == 200 else False

    @classmethod
    def create_index(cls, user_id, id, idx_object):
        obj = idx_object.to_dict()
        # XXX Create mappings (in children classes)
        return cls.create(user_id, id, obj)

    @classmethod
    def filter(cls, user_id, params, order=None, limit=None):
        # XXX well I know this it bad, security must be considered strongly
        index_server_url = get_component(IStorageIndex).get_connection()
        values = []
        for k, v in params.iteritems():
            if k.endswith('_id'):
                values.append('%s:%s' % (k, v))
            else:
                values.append('%s = %s' % (k, v))
        q_str = ' AND '.join(values)
        query = {
            "query": {
                "filtered": {
                    "query": {
                        "query_string": {
                            "query": q_str
                        }
                    }
                }
            }
        }
        if limit:
            query.update({
                'from': limit.get('from', 0),
                'size': limit.get('size', 10),
            })
        route = "%s/%s/%s/_search?" % (index_server_url, user_id, cls.type)
        res = requests.get(route, data=to_json(query))
        data = res.json()
        results = []
        for idx in data.get('hits', []).get('hits', []):
            results.append(cls(idx['_source']))
        return results

    def to_dict(self):
        data = {}
        for col in self.columns:
            # XXX only not none columns ?
            data.update({col: getattr(self, col)})
        return data


class BaseIndexMessage(BaseIndexDocument):
    """Base class to store a message in an index store"""
    columns = ['message_id', 'thread_id', 'security_level',
               'subject', 'from_', 'date', 'date_insert',
               'text', 'size', 'answer_to', 'offset', 'headers',
               'tags', 'markers', 'parts', 'contacts',
               ]


@implementer(IMailIndexMessage)
class MailIndexMessage(BaseIndexMessage):
    """Get a user message object, and parse it to make an index"""

    def __init__(self, message, thread_id, message_id, answer_to, offset):
        self.message_id = message_id
        self.thread_id = thread_id
        self.answer_to = answer_to
        self.offset = offset
        self.security_level = message.security_level
        self.date_insert = datetime.utcnow()
        self._parse_message(message)
        self._parse_parts(message.parts)
        cts = [x.to_dict() for x in message.recipients]
        self.contacts = cts
        self.tags = message.tags

    def _parse_message(self, message):
        self.subject = message.subject
        self.from_ = message.contact_from.contact_id
        self.date = message.date
        self.text = message.text
        self.size = message.size
        self.headers = message.headers
        self.markers = ['U']

    def _parse_parts(self, parts):
        self.parts = []
        for part in [x for x in parts if x.can_index()]:
            self.parts.append({'id': part.id,
                               'size': part.size,
                               'content_type': part.content_type,
                               'filename': part.filename,
                               'content': part.payload})


class TagMixin(object):
    """Mixin for indexed objects havings tags"""

    def add_tag(self, tag):
        if tag in self.tags:
            return False
        query = {
            'script': 'ctx._source.tags += tag',
            'params': {'tag': tag}
        }
        self.update(query)
        self.refresh()
        return True

    def remove_tag(self, tag):
        if not tag in self.tags:
            return False
        query = {
            'script': 'ctx._source.tags -= tag',
            'params': {'tag': tag}
        }
        self.update(query)
        self.refresh()
        return True

    def set_tags(self, tags):
        if tags == self.tags:
            return False
        query = {
            'script': 'ctx._source.tags = tags',
            'params': {'tags': tags}
        }
        self.update(query)
        self.refresh()
        return True


@implementer(IIndexedMessage)
class IndexedMessage(BaseIndexMessage, TagMixin):
    """Message from index server with helpers methods"""

    type = 'messages'


@implementer(IIndexedContact)
class IndexedContact(BaseIndexDocument, TagMixin):
    """Contact from index server with helpers methods"""

    def __init__(self, data):
        # Index everything
        for k, v in data.iteritems():
            setattr(self, k, v)

    type = 'contacts'


@implementer(IIndexedThread)
class IndexedThread(BaseIndexDocument, TagMixin):
    """Thread from index server"""

    columns = ['thread_id', 'date_insert', 'date_update',
               'security_level', 'slug', 'tags', 'contacts']

    type = 'threads'
