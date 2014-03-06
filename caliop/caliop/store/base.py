from datetime import datetime

import requests

from caliop.config import Configuration
from caliop.helpers.log import log
from caliop.helpers.json import to_json


class AbstractIndex(object):
    """Abstract class for indexed objects"""
    # XXX : automagic server discovery differently ....
    index_server_url = Configuration('global').get('index_server.url')

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
        route = "%s/%s/%s/%s" % (cls.index_server_url, user_id, cls.type, uid)
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
        route = '%s/%s/%s/%s' % (cls.index_server_url, user_id, cls.type, id)
        res = requests.put(route, to_json(data))
        return True if res.status_code == 200 else False

    @classmethod
    def create_index(cls, user_id, id, idx_object):
        obj = idx_object.to_dict()
        # XXX Create mappings (in children classes)
        return cls.create(user_id, id, obj)

    @classmethod
    def filter(cls, user_id, params):
        # XXX well I know this it bad, security must be considered strongly
        values = ["%s:%s" % (k, v) for k, v in params.iteritems()]
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
        route = "%s/%s/%s/_search?" % (cls.index_server_url, user_id, cls.type)
        res = requests.get(route, data=to_json(query))
        data = res.json()
        if data.get('hits', {}).get('hits'):
            return [cls(x['_source'])
                    for x in data['hits']['hits']]
        return []

    def to_dict(self):
        data = {}
        for col in self.columns:
            # XXX only not none columns ?
            data.update({col: getattr(self, col)})
        return data


class UserIndex(AbstractIndex):
    """Only here to manage user index globally (create, delete)"""

    @classmethod
    def create(cls, user):
        # Create index for user
        route = '%s/%s' % (cls.index_server_url, user.id)
        res = requests.put(route)
        return True if res.status_code == 200 else False


class BaseIndexMessage(AbstractIndex):
    """Base class to store a message in an index store"""
    columns = ['message_id', 'thread_id', 'security_level',
               'subject', 'from_', 'date', 'date_insert',
               'text', 'size', 'headers',
               'tags', 'markers', 'parts', 'contacts',
               ]

    def __init__(self, message):
        for col in self.columns:
            setattr(self, col, message.get(col))


class MailIndexMessage(BaseIndexMessage):
    """Get a user message object, and parse it to make an index"""

    def __init__(self, message, thread_id, message_id):
        self.message_id = message_id
        self.thread_id = thread_id
        self.security_level = message.security_level
        self.date_insert = datetime.utcnow()
        self._parse_message(message)
        self._parse_parts(message.parts)
        self.contacts = [x.contact_id for x in message.contacts]
        self.tags = message.tags

    def _parse_message(self, message):
        self.subject = message.mail.get('Subject')
        self.from_ = message.contact_from.contact_id
        self.date = message.date
        self.text = message.text
        self.size = message.size
        self.headers = message.headers
        self.markers = ['U']

    def _parse_parts(self, parts):
        self.parts = {}
        for part in parts:
            self.parts.update({'id': part.id,
                               'size': part.size,
                               'content_type': part.content_type,
                               'filename': part.filename,
                               'content': part.get_text()})
