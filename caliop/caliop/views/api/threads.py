# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from .api import API



class Thread(API):
    filename = 'threads.json'

    def init(self):
        self.users = json.loads(self.read_json(filename='users.json'))
        self.tags = json.loads(self.read_json(filename='tags.json'))

    def _augment(self, thread):
        """
        Add users, tags.
        """
        # link users
        thread_users = filter(lambda r: r['id'] in thread['users'],
                                    self.users)
        thread['users'] = thread_users

        # link tags
        thread_tags = filter(lambda l: l['id'] in thread['tags'],
                                    self.tags)
        thread['tags'] = thread_tags

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

        # keep only threads of the logged user
        threads = [thread for thread in threads
                    if self.user['id'] in thread['users']]

        # filter by tags
        tags_id = [int(id_) for id_ in self.request.GET.getall('tag')]
        if tags_id:
            threads = [thread for thread in threads
                # if intersection == number of tags
                if len(set(tags_id).intersection(
                    set(thread['tags']))) == len(tags_id)]

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


class TagsToThreads(API):
    filename = 'threads.json'

    def put(self):
        """
        Add tags to threads.
        """
        json_ = self.request.json
        threads = json.loads(self.read_json(filename='threads.json'))

        for thread_id in json_['threads']:
            threads_ = [t for t in threads if t['id'] == thread_id]

            if len(threads_):
                thread = threads_[0]
                thread['tags'] = json_['tags'] if 'tags' in json_ else []
                self.update_to_json(thread_id, thread)

        return Response(json.dumps({
            'success': 'true'
        }))



