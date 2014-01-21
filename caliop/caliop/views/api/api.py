from __future__ import absolute_import, unicode_literals


import os
import json

from pyramid.response import Response


class Api(object):
    filename = None
    request = None

    def __init__(self, request):
        self.request = request

    def get_path(self, **kw):
        rootpath = os.path.dirname(os.path.realpath(__file__))
        filename = kw.get('filename', self.filename)
        return os.path.join(rootpath, 'json', filename)

    def read_json(self, **kw):
        filename = kw.get('filename', self.filename)
        path = self.get_path(filename=filename)

        stream = open(path)
        json = stream.read()
        stream.close()

        return json

    def __call__(self):
        return Response(self.read_json())


class Threads(Api):
    filename = 'threads.json'

    def __call__(self):
        recipients = json.loads(self.read_json(filename='recipients.json'))
        threads = json.loads(self.read_json())

        # link recipients to each threads
        for thread in threads:
            thread_recipients = filter(lambda r: r['id'] in thread['recipients'],
                                       recipients)
            thread['recipients'] = thread_recipients

        return Response(json.dumps(threads))


class Messages(Api):
    filename = 'messages.json'


class ContactLogin(Api):
    filename = 'contact.json'

    def __call__(self):
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            if (credentials['login'] == 'bad' and credentials['password'] == 'bad'):
                raise BadCredentials

            return Response(self.read_json())

        except (KeyError, BadCredentials):
            return Response('BadCredentials', status='403 Forbidden')


class ContactInfo(Api):
    filename = 'contact.json'
