#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import yaml

try:
    from yaml import CSafeLoader as YAMLLoader
except ImportError:
    from yaml import SafeLoader as YAMLLoader


class Configuration(object):
    """ Configuration store. """

    _conffiles = {}
    _filename = None

    def __init__(self, name):
        self._name = name

    @classmethod
    def load(cls, filename, name=None):
        """
        Loads configuration from `filename`.
        An optional `name` is recommended to use many environment.
        """
        name = name or filename

        if name not in cls._conffiles:
            with open(filename) as fdesc:
                cls._conffiles[name] = yaml.load(fdesc, YAMLLoader)
        return cls(name)

    @property
    def configuration(self):
        """ Get the configuration for current object.

        .. deprecated:: use the :meth:`get` instead
        """
        return self._conffiles[self._name]

    def get(self, key, default=None):
        """ Retrieve a configuration setting.

        :param key: a dot separated string
        :type key: str
        """
        key = key.split('.')
        value = self.configuration
        try:
            for k in key:
                value = value[k]
            return value
        except KeyError:
            return default
