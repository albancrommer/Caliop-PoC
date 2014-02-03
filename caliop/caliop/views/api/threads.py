from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API



class Thread(API):
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

    def get(self):
        thread_id = int(self.request.matchdict.get('thread_id'))

        threads = json.loads(self.read_json())
        thread = filter(lambda t: int(t['id']) == thread_id, threads).pop()

        self.augment(thread)

        return Response(json.dumps(thread))


class Threads(Thread):
    def get(self):
        threads = json.loads(self.read_json())

        for thread in threads:
            self.augment(thread)

        return Response(json.dumps(threads))