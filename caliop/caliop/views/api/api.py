from __future__ import absolute_import, unicode_literals


import os
import json

from pyramid.response import Response


class Api(object):
    filename = None
    request = None

    def __init__(self, request):
        self.request = request
        self.init()

    def init(self):
        pass

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


class Thread(Api):
    filename = 'threads.json'

    def init(self):
        self.recipients = json.loads(self.read_json(filename='recipients.json'))
        self.labels = json.loads(self.read_json(filename='labels.json'))

    def augment(self, thread):
        """
        Add recipient, labels.
        """

        # link recipients
        thread_recipients = filter(lambda r: r['id'] in thread['recipients'],
                                   self.recipients)
        thread['recipients'] = thread_recipients

        # link labels
        thread_labels = filter(lambda l: l['id'] in thread['labels'],
                                   self.labels)
        thread['labels'] = thread_labels

    def __call__(self):
        thread_id = int(self.request.matchdict.get('thread_id'))

        threads = json.loads(self.read_json())
        thread = filter(lambda t: int(t['id']) == thread_id, threads).pop()

        self.augment(thread)

        return Response(json.dumps(thread))


class Threads(Thread):
    def __call__(self):
        threads = json.loads(self.read_json())

        for thread in threads:
            self.augment(thread)

        return Response(json.dumps(threads))


class ThreadMessages(Api):
    filename = 'messages.json'

    def __call__(self):
        from pprint import pprint

        messages = json.loads(self.read_json())
        recipients = json.loads(self.read_json(filename='recipients.json'))

        thread_id = int(self.request.matchdict.get('thread_id'))

        # grep messages of the wanted thread
        filtered_messages = filter(lambda m: m['thread_id'] == thread_id, messages)

        for message in filtered_messages:
            # link author
            message['author'] = filter(lambda r: r['id'] == message['author'],
                                       recipients).pop()

        return Response(json.dumps(filtered_messages))


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
