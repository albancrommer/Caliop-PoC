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
