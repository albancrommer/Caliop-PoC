from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API



class Users(API):
    filename = 'users.json'

    def post(self):
        user = self.request.json
        id = self.add_to_json(user)
        return Response(json.dumps({
            'success': 'true',
            'user_id': id
        }))

    def get(self):
        users = json.loads(self.read_json())
        groups = json.loads(self.read_json(filename='groups.json'))

        for user in users:
            user['groups'] = [group for group in groups if group['id']
                                in user['groups']]

        return Response(json.dumps(users))
