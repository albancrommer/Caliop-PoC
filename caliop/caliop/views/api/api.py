from __future__ import absolute_import, unicode_literals


import os
import json

from pyramid.response import Response


class Api(object):
    def __init__(self, request):
        self.request = request

    def get_json(self):
        rootpath = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(rootpath, 'json', self.filename)

    def __call__(self):
        with open(self.get_json()) as jsonfile:
            response = Response(jsonfile.read())

        return response


class Messages(Api):
    filename = 'messages.json'


class ContactLogin(Api):
    filename = 'contact.json'

    def __call__(self):
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            if (credentials['login'] == 'c' and credentials['password'] == 'c'):
                with open(self.get_json()) as jsonfile:
                    response = Response(jsonfile.read())

                return response
            else:
                raise BadCredentials
        except (KeyError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')


class ContactInfo(Api):
    filename = 'contact.json'
