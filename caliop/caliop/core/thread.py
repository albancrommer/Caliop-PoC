# XXX : define our own exceptions ?
from cqlengine.query import DoesNotExist

from caliop.core.base import AbstractCore
from caliop.store import ThreadLookup as ModelThreadLookup


class ThreadLookup(AbstractCore):

    _model_class = ModelThreadLookup

    @classmethod
    def get(cls, user, external_id):
        try:
            return cls._model_class.get(user_id=user.id, id=external_id)
        except DoesNotExist:
            return None
