from caliop.store.base import AbstractIndex, BaseIndexMessage


class TagMixin(object):
    """Mixin for indexed objects havings tags"""

    def add_tag(self, tag):
        if tag in self.tags:
            return False
        query = {
            'script': 'ctx._source.tags += tag',
            'params': {'tag': tag}
        }
        self.update(query)
        self.refresh()
        return True

    def remove_tag(self, tag):
        if not tag in self.tags:
            return False
        query = {
            'script': 'ctx._source.tags -= tag',
            'params': {'tag': tag}
        }
        self.update(query)
        self.refresh()
        return True

    def set_tags(self, tags):
        if tags == self.tags:
            return False
        query = {
            'script': 'ctx._source.tags = tags',
            'params': {'tags': tags}
        }
        self.update(query)
        self.refresh()
        return True


class IndexedMessage(BaseIndexMessage, TagMixin):
    """Message from index server with helpers methods"""

    type = 'messages'


class IndexedContact(AbstractIndex, TagMixin):
    """Contact from index server with helpers methods"""

    def __init__(self, data):
        # Index everything
        for k, v in data.iteritems():
            setattr(self, k, v)

    type = 'contacts'


class IndexedThread(AbstractIndex, TagMixin):
    """Thread from index server"""

    columns = ['thread_id', 'date_insert', 'date_update',
               'slug', 'tags', 'contacts']

    type = 'threads'
