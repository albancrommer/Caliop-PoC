# -*- coding: utf-8 -*-
"""
Caliop storage interface
"""

from __future__ import absolute_import, print_function, unicode_literals

from zope.interface import Attribute, Interface


class ICaliop(Interface):
    """ The Caliop head interface that need to be adapted """


class IStorage(Interface):
    """ Data storage """

    def initialize_db(cls, settings):
        """
        Create the schema
        """

    def connect(cls, settings):
        """
        Connect to the storage.
        """

    def disconnect(cls):
        """
        Disconnect to the storage.
        """

    def get_connection(cls):
        """
        Return a connection to the database
        """


class IStorageIndex(Interface):
    """ Search Engine """

    def initialize_db(cls, settings):
        """
        Create the search engine schema
        """

    def connect(cls, settings):
        """
        Connect to the storage.
        """

    def disconnect(cls):
        """
        Disconnect to the storage.
        """

    def get_connection(cls):
        """
        Return a connection to the database
        """


class IStorable(Interface):

    def validate(self):
        """ return True if the object is storable in it's current state
        otherwise raises a ModelErrors exception"""
