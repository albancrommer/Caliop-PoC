import bcrypt

from caliop.core.base import AbstractCore
from caliop.core.contact import ContactLookup
from caliop.store import User as ModelUser, Counter as ModelCounter, UserIndex


class Counter(AbstractCore):

    _model_class = ModelCounter
    _pkey_name = 'user_id'


class User(AbstractCore):

    _model_class = ModelUser

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop('password')
        kwargs['password'] = bcrypt.hashpw(password, bcrypt.gensalt())
        user = super(User, cls).create(**kwargs)
        # Create counters
        Counter.create(user_id=user.id)
        # Create index
        UserIndex.create(user)
        return user

    @classmethod
    def authenticate(cls, uid, password):
        user = cls._model_class.get(id=uid)
        if bcrypt.hashpw(password, user.password) == user.password:
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


class UserMessage(object):
    """Class to use for creating thread and message in store"""

    def __init__(self, user, message, security_level, contacts, tags, parts):
        self.user = user
        self.message = message
        self.security_level = security_level
        self.contacts = contacts
        self.tags = tags
        self.parts = parts
        self.external_message_id = self.message.message_id
        self.external_thread_id = self.message.thread_id
        self.contact_from = ContactLookup.get(user, message.from_)
        self.text = message.text
        self.date = message.date
        self.mail = message.mail
        self.size = message.size
        self.headers = message.headers
