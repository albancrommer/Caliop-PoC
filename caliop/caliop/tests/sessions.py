from __future__ import unicode_literals

import unittest
import json

from pyramid import testing

from caliop.views.api.sessions import Sessions


class TestViewSessions(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test01_post_sessions_ok(self):
        """
        When POSTING valid credentials, it should return a dict.
        """

        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = {'login': 'aze', 'password': 'aze'}
        request.context = testing.DummyResource()
        response = Sessions(request)()
        json_ = json.loads(response.text)

        self.assertEqual(json_, {
            u'lastName': u'Rocks',
            u'id': 1,
            u'firstName': u'Gandi',
            u'date_created': u'2013-15-01 14:51:21'})

    def test01_post_sessions_ko(self):
        """
        When POSTING bad credentials, it should return a 403.
        """

        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = {'login': 'bad', 'password': 'bad'}
        request.context = testing.DummyResource()
        response = Sessions(request)()

        self.assertEqual(response.status, '403 Forbidden')

    def test01_delete_sessions(self):
        request = testing.DummyRequest()
        request.method = 'DELETE'
        request.context = testing.DummyResource()
        response = Sessions(request)()
        json_ = json.loads(response.text)

        self.assertEqual(json_, {u'status': u'logout'})

