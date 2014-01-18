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
        return Response(open(self.get_json()).read())


class Messages(Api):
    filename = 'messages.json'


class ContactLogin(Api):
    filename = 'contact.json'

    def __call__(self):
        params = self.request.POST.mixed().keys()[0]    # wtf ?
        credentials = json.loads(params)

        class BadCredentials(Exception):
            pass

        try:
            if (credentials[u'login'] == 'c' and credentials[u'password'] == 'c'):
                return Response(open(self.get_json()).read())
            else:
                raise BadCredentials
        except (AttributeError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')


class ContactInfo(Api):
    filename = 'contact.json'
