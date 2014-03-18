# -*- coding: utf-8 -*-
"""
Caliop core base class.

Core are glue code to the storage abstraction layer.
"""

from __future__ import absolute_import, print_function, unicode_literals

from cqlengine import columns


class BaseCore(object):
    """Base class for all core objects"""
    _model_class = None
    _pkey_name = 'id'

    def __init__(self, obj):
        self.model = obj

    @classmethod
    def create(cls, **kwargs):
        obj = cls._model_class.create(**kwargs)
        return cls(obj)

    @classmethod
    def get(cls, key):
        params = {cls._pkey_name: key}
        obj = cls._model_class.get(**params)
        if obj:
            return cls(obj)
        raise Exception('%s %d not found' % (cls._model_class.__name__, key))

    def save(self):
        return self.model.save()

    def __getattr__(self, attr):
        if attr in self.model._columns.keys():
            col = getattr(self.model, attr)
            if isinstance(self.model._columns[attr], columns.UUID):
                return str(col)
            return col
