from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API



class Sessions(API):
    filename = 'users.json'

    def post(self):
        """
        Login.
        """
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            # search a user matching login=first_name and password=last_name
            users = json.loads(self.read_json())

            foundUsers = [user for user in users \
                if user['first_name'] == credentials['login'] \
                and user['last_name'] == credentials['password']]

            if not foundUsers:
                raise BadCredentials

            return Response(json.dumps(foundUsers[0]))

        except (KeyError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')

    def delete(self):
        """
        Logout.
        """
        return Response(json.dumps({'status': 'logout'}))


class ContactInfo(API):
    filename = 'contact.json'
