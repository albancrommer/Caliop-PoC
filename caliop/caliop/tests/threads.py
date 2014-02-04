from __future__ import unicode_literals

import unittest
import json

from pyramid import testing

from caliop.views.api.threads import Threads


class TestViewThreads(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test01_delete_threads_not_allowed(self):
        """
        Can't delete a thread.
        """

        request = testing.DummyRequest()
        request.method = 'DELETE'
        request.context = testing.DummyResource()
        response = Threads(request)()

        self.assertEqual(response.status, '405 Method Not Allowed')

    def test02_get_threads(self):
        """
        Retrieve the list of threads.
        """

        request = testing.DummyRequest()
        request.method = 'GET'
        request.context = testing.DummyResource()
        response = Threads(request)()

        threads = json.loads(response.text)

        self.assertGreaterEqual(len(threads), 1)
        self.assertEqual('This is my first message.', threads[0]['text'])



    def test03_post_thread(self):
        """
        Add a thread to the JSON file.
        """
        # count threads
        request = testing.DummyRequest()
        request.method = 'GET'
        request.context = testing.DummyResource()
        response = Threads(request)()
        threads = json.loads(response.text)

        # save a new thread
        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = {
            "id": (threads[-1]['id'] + 1),
            "date_updated": "2013-10-14 12:52:00",
            "text": "To take a trivial example, which of us ever undertakes laborious physical exercise.",
            "security": 75,
            "users": [1],
            "labels": [1],
        }
        response = Threads(request)()

        response_text = json.loads(response.text)
        self.assertTrue(response_text['success'], 'true')
        self.assertTrue(response_text['thread_id'], len(threads) +1)

        # Check than the user has been saved
        request = testing.DummyRequest()
        request.method = 'GET'
        response = Threads(request)()
        threads = json.loads(response.text)

        self.assertTrue(len(threads), len(threads)+1)
        self.assertTrue('To take a trivial example, which of us ever undertakes laborious physical exercise.',
            threads[-1]['text'])
