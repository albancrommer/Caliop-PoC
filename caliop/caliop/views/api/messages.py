# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API



class Messages(API):
    filename = 'messages.json'

    def get(self):
        """
        Retrieve the list of messages for a given thread.
        """
        messages = json.loads(self.read_json())
        users = json.loads(self.read_json(filename='users.json'))

        thread_id = int(self.request.matchdict.get('thread_id'))

        # grep messages of the wanted thread
        filtered_messages = filter(lambda m: m['thread_id'] == thread_id, messages)

        for message in filtered_messages:
            # link author
            message['author'] = filter(lambda r: r['id'] == message['author'],
                                       users).pop()

        return Response(json.dumps(filtered_messages))

    def post(self):
        """
        Create a new message.
        """
        message = self.request.json
        message['thread_id'] = int(self.request.matchdict.get('thread_id'))

        id = self.add_to_json(message)

        return Response(json.dumps({
            'success': 'true',
            'message_id': id
        }))
