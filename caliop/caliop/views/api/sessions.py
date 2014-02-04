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
            if (credentials['login'] == 'bad' and credentials['password'] == 'bad'):
                raise BadCredentials

            # for the moment, the first user if the authed contact
            users = json.loads(self.read_json())
            return Response(json.dumps(users[0]))

        except (KeyError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')

    def delete(self):
        """
        Logout.
        """
        return Response(json.dumps({'status': 'logout'}))


class ContactInfo(API):
    filename = 'contact.json'
