from caliop.store.base import BaseIndexMessage


class IndexedMessage(BaseIndexMessage):
    """Message from index server with helpers methods"""

    type = 'message'

    def __init__(self, user_id, uid):
        self.get(user_id, uid)
        self.user_id = user_id
        self.uid = uid

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
