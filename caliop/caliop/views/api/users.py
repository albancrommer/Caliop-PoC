from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API



class Users(API):
    filename = 'users.json'

    def get(self):
        users = json.loads(self.read_json())
        groups = json.loads(self.read_json(filename='groups.json'))

        for user in users:
            user['groups'] = [group for group in groups if group['id']
                                in user['groups']]

        return Response(json.dumps(users))
