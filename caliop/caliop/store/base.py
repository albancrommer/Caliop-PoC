from dateutil.parser import parse as parse_date
from email.message import Message as mailMessage

import json
import requests

from caliop.config import Configuration


class AbstractIndex(object):
    """Abstract class for indexed objects"""
    # XXX : automagic server discovery differently ....
    index_server_url = Configuration('global').get('index_server.url')

    columns = []
    type = None

    def __init__(self, data):
        for col in self.columns:
            setattr(self, col, data.get(col, None))

    def get(self, user_id, uid):
        route = "%s/%s/%s/%s" % (self.index_server_url, user_id, self.type, id)
        res = requests.get(route)
        if res.status_code == 200:
            message = res.json()
            for col in self.columns:
                setattr(self, col, message[col])
        raise Exception('Index %s/%s/%s not found' % (user_id, self.type, id))

    def refresh(self):
        self.get(self.user_id, self.uid)

    def update(self, query):
        route = "%s/%s/%s/%s/_update" % \
            (self.index_server_url, self.user_id, self.type, self.uid)
        res = requests.post(route, data=json.dumps(query))
        return True if res.status_code == 200 else False

    @classmethod
    def create_index(cls, user_id, id, idx_object):
        route = '%s/%s/%s/%s' % (cls.index_server_url, user_id, cls.type, id)
        obj = idx_object.to_json()
        res = requests.put(route, obj)
        return True if res.status_code == 200 else False

    @classmethod
    def filter(cls, user_id, params):
        values = ["%s = %s" % (k, v) for k, v in params.iteritems()]
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
        route = "%s/%s/%s/_search?" % (cls.index_server_url, cls.type, user_id)
        res = requests.get(route, data=json.dumps(query))
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
    columns = ['subject', 'from_', 'to', 'cc', 'bcc',
               'date', 'message_id', 'thread_id', 'slug', 'size',
               'tags', 'markers']

    def __init__(self, message):
        for col in self.columns:
            setattr(self, col, message.get(col))


class MailIndexMessage(BaseIndexMessage):
    """Get a mail message object, and parse it to make an index"""

    def __init__(self, mail):
        if not isinstance(mail, mailMessage):
            raise Exception('Invalid mail')
        self._parse_mail(mail)

    def _parse_mail(self, mail):
        self.subject = mail.get('Subject')
        self.headers = dict((k, v) for k, v in mail.items())
        self.from_ = mail.get('From')
        self.to = mail.get('To')
        self.cc = mail.get('CC')
        self.bcc = mail.get('Bcc')
        self.date = parse_date(mail.get('Date'))
        self.message_id = mail.get('Message-Id')
        self.thread_id = mail.get('Thread-Id')
        self.slug = mail.get_payload()[:200]
        self.size = len(mail.get_payload())
        self.tags = ['MAIL', 'INBOX']
        self.markers = ['U']
