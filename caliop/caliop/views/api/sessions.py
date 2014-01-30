from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPMethodNotAllowed

from .api import API



class Sessions(API):
    filename = 'contact.json'

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

            return Response(self.read_json())

        except (KeyError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')

    def delete(self):
        """
        Logout.
        """
        return Response(json.dumps({'status': 'logout'}))

    def __call__(self):
        if self.request.method in ('POST', 'DELETE'):
            return getattr(self, self.request.method.lower())()

        else:
            return HTTPMethodNotAllowed()


class ContactInfo(API):
    filename = 'contact.json'
