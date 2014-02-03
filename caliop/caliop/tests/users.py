from __future__ import unicode_literals

import unittest
import json

from pyramid import testing

from caliop.views.api.users import Users


class TestViewUsers(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test01_get_users(self):
        """
        Retrieve the list of users.
        """

        request = testing.DummyRequest()
        request.method = 'GET'
        request.context = testing.DummyResource()
        response = Users(request)()

        users = json.loads(response.text)

        self.assertGreaterEqual(len(users), 6)
        self.assertTrue('Danjou', users[0]['last_name'])

    def test02_post_user(self):
        """
        Add a user to JSON file.
        """

        # save a new user
        request = testing.DummyRequest()
        request.method = 'POST'
        request.json = {
            "first_name": "Foo",
            "last_name": "Bar",
            "connected": True,
            "groups": [1],
            "message": "Sample test",
            "id": 7
        }
        request.context = testing.DummyResource()
        response = Users(request)()

        status = json.loads(response.text)
        self.assertTrue('ok', status)

        # Check than the user has been saved
        request = testing.DummyRequest()
        request.method = 'GET'
        request.context = testing.DummyResource()
        response = Users(request)()

        users = json.loads(response.text)

        self.assertGreaterEqual(len(users), 7)
        self.assertTrue('Foo', users[-1]['first_name'])


