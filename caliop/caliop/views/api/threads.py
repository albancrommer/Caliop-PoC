from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from .api import API



class Thread(API):
    filename = 'threads.json'

    def init(self):
        self.users = json.loads(self.read_json(filename='users.json'))
        self.labels = json.loads(self.read_json(filename='labels.json'))

    def _augment(self, thread):
        """
        Add users, labels.
        """
        # link users
        thread_users = filter(lambda r: r['id'] in thread['users'],
                                   self.users)
        thread['users'] = thread_users

        # link labels
        thread_labels = filter(lambda l: l['id'] in thread['labels'],
                                   self.labels)
        thread['labels'] = thread_labels

    def get(self):
        """
        Retrieve a thread.
        """
        thread_id = int(self.request.matchdict.get('thread_id'))

        threads = json.loads(self.read_json())
        thread = filter(lambda t: int(t['id']) == thread_id, threads).pop()

        self._augment(thread)

        return Response(json.dumps(thread))

    def put(self):
        """
        Update an existing thread.
        """
        thread_id = int(self.request.matchdict.get('thread_id'))
        thread = self.request.json
        thread_data = self.update_to_json(thread_id, thread)

        if not thread_data:
            return HTTPNotFound()
        else:
            return Response(json.dumps(thread_data))

class Threads(Thread):
    def get(self):
        threads = json.loads(self.read_json())

        for thread in threads:
            self._augment(thread)

        return Response(json.dumps(threads))

    def post(self):
        """
        Create a new empty thread.
        """
        thread = self.request.json
        id = self.add_to_json(thread)

        return Response(json.dumps({
            'success': 'true',
            'thread_id': id
        }))
