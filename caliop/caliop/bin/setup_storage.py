#!/usr/bin/env python
"""
This script create cassandra models in a local cassandra instance.

This should be abstracted in a backend to get many backend supported.
"""


def setup_storage(settings):
    from caliop.config import Configuration
    from caliop.storage import registry
    from caliop.storage.data.interfaces import IStorage

    registry.configure(Configuration('global'))
    registry.get_component(IStorage).initialize_db(settings)

