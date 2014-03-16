import bcrypt
from datetime import datetime

from caliop.helpers.config import Configuration

from caliop.core.base import AbstractCore
from caliop.core.contact import ContactLookup
from caliop.store import (User as ModelUser,
                          Tag as ModelTag,
                          Counter as ModelCounter,
                          UserIndex)


class Counter(AbstractCore):

    _model_class = ModelCounter
    _pkey_name = 'user_id'


class Tag(AbstractCore):

    _model_class = ModelTag

    @classmethod
    def get(cls, user, id):
        return cls(cls._model_class.get(user_id=user.id, label=id))

    def to_api(self):
        return {
            'id': 1,    # TOFIX
            'label': self.label,
            'background': self.background,
            'color': self.color,
        }


class User(AbstractCore):

    _model_class = ModelUser

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password')
        kwargs['password'] = bcrypt.hashpw(password, bcrypt.gensalt())
        kwargs['date_insert'] = datetime.utcnow()
        user = super(User, cls).create(**kwargs)
        # Create counters
        Counter.create(user_id=user.id)
        # Create default tags
        default_tags = Configuration('global').get('system.default_tags')
        for tag in default_tags:
            Tag.create(user_id=user.id, **tag)
        # Create index
        UserIndex.create(user)
        return user

    @classmethod
    def authenticate(cls, uid, password):
        user = cls._model_class.get(id=uid)
        # XXX : decode unicode not this way
        if bcrypt.hashpw(str(password), str(user.password)) == user.password:
            return cls(user)
        raise Exception('Invalid credentials')

    def new_message_id(self):
        counter = Counter.get(self.id)
        # XXX : MUST be handled by core object correctly
        counter.model.message_id += 1
        counter.save()
        return counter.message_id

    def new_thread_id(self):
        counter = Counter.get(self.id)
        # XXX : MUST be handled by core object correctly
        counter.model.thread_id += 1
        counter.save()
        return counter.thread_id

    def get_thread_id(self, external_id):
        # XXX : lookup external thread_id to internal one
        return self.new_thread_id()

    def to_api(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_created': self.date_insert,
        }

    @property
    def tags(self):
        objs = Tag._model_class.objects.filter(user_id=self.id)
        return [Tag(x) for x in objs]


class UserMessage(object):
    """Class to use for creating thread and message in store"""

    def __init__(self, user, message, security_level, recipients, tags, parts):
        self.user = user
        self.subject = message.subject
        self.message = message
        self.security_level = security_level
        self.recipients = recipients
        self.tags = tags
        self.parts = parts
        self.external_message_id = self.message.message_id
        self.external_parent_id = self.message.parent_message_id
        from_addr = message.recipients['from'][0]
        self.contact_from = ContactLookup.get(user, from_addr[0])
        self.text = message.text
        self.date = message.date
        self.size = message.size
        self.headers = message.headers
