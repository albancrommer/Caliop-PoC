
from caliop.config import Configuration
from caliop.storage import registry
from caliop.storage.data.interfaces import IStorage

def includeme(config):

    registry.configure(Configuration('global'))
    registry.get_component(IStorage).connect(config.registry.settings)
