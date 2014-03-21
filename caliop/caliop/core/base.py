# -*- coding: utf-8 -*-
"""
Caliop core base class.

Core are glue code to the storage abstraction layer.
"""

from __future__ import absolute_import, print_function, unicode_literals


class BaseCore(object):
    """Base class for all core objects"""
    _model_class = None
    _lookup_classes = {}
    _index_class = None
    _pkey_name = 'id'

    def __init__(self, model):
        self.model = model

    @classmethod
    def create(cls, **kwargs):
        indexed_extra = kwargs.pop('_indexed_extra', {})
        obj = cls._model_class.create(**kwargs)
        for lookup in cls._lookup_classes.values():
            lookup.create(obj, **kwargs)

        obj = cls(obj)
        if cls._index_class:
            cls._index_class.create(obj, **indexed_extra)
        return obj

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
        """
        used to proxy model attribute.
        Does not proxy attributed retrieve via a "lookup".
        """
        if attr in self.model._columns.keys():
            return getattr(self.model, attr)
