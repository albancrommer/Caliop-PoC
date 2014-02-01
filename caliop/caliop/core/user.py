import bcrypt

from caliop.core.base import AbstractCore
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
        return cls(user)

    @classmethod
    def authenticate(cls, uid, password):
        user = cls._model_class.get(id=uid)
        if bcrypt.hashpw(password, user.password) == user.password:
            return cls(user)
        raise Exception('Invalid credentials')