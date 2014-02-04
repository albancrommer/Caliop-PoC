from __future__ import unicode_literals

import unittest
import json

from pyramid import testing

from caliop.views.api.messages import Messages


class TestViewMessages(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test01_get_messages(self):
        """
        Retrieve the list of messages of a thread.
        """

        request = testing.DummyRequest()
        request.matchdict = {'thread_id': 1}
        request.method = 'GET'
        request.context = testing.DummyResource()
        response = Messages(request)()

        messages = json.loads(response.text)

        self.assertEqual(len(messages), 6)
        self.assertEqual(messages[0]['title'], 'Hello Caliop')

    def test02_post_message(self):
        """
        Add a message to the JSON file.
        """
        # count all messages
        request = testing.DummyRequest()
        request.method = 'GET'
        request.matchdict = {'thread_id': 1}
        request.context = testing.DummyResource()
        all_messages = json.loads(Messages(request).read_json())

        # save a new message
        request = testing.DummyRequest()
        request.matchdict = {'thread_id': 1}
        request.method = 'POST'
        request.json = {
            "id": (all_messages[-1]['id'] + 1),
            "body": "Donec tempus risus quis neque rhoncus euismod. Donec nec metus non velit facilisis consequat at a urna.",
            "author": 4,
            "protocole": "email",
            "title": "yeah!",
            "offset": 0,
            "thread_id": 1,
            "answer_to": 0,
            "date_sent": "2013-10-01 15:02:10",
            "security": 50,
        }
        response = Messages(request)()

        response_text = json.loads(response.text)
        self.assertTrue(response_text['success'], 'true')
        self.assertTrue(response_text['message_id'], len(all_messages) +1)

        # Check than the message has been saved
        request = testing.DummyRequest()
        request.matchdict = {'thread_id': 1}
        request.method = 'GET'
        all_messages2 = json.loads(Messages(request).read_json())

        self.assertTrue(len(all_messages2), len(all_messages)+1)
        self.assertTrue('Donec tempus risus quis neque rhoncus euismod. Donec nec metus non velit facilisis consequat at a urna.',
            all_messages2[-1]['body'])
