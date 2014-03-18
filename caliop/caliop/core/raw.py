import hashlib


from caliop.storage.data.cassandra import RawMail as ModelRawMail
from caliop.core.base import BaseCore


class RawMail(BaseCore):

    _model_class = ModelRawMail

    @classmethod
    def create(cls, message_id, users, raw):
        key = hashlib.sha256(message_id).hexdigest()
        return super(RawMail, cls).create(raw_id=key, users=users, data=raw)
