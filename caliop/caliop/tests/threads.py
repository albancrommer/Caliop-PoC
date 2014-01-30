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

        self.assertEqual(len(threads), 11)
        self.assertTrue(
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit'
            in threads[0]['text'])
