.. -*- coding: utf-8 -*-
.. $Id$
.. vim:  ts=4 sw=4 smarttab expandtab syntax=rst

========================
REST API Documentation
========================

.. note::

  All methods accept an ``application/json`` header and return an
  ``application/json`` content-type.

  Caliopen API will render the response in JSON format following the current REST
  API specifications.


.. seealso::

  RESTful API best pratices: http://stackoverflow.com/questions/2001773/understanding-rest-verbs-error-codes-and-authentication/2022938#2022938


.. http:post:: /sessions

   Create a new session which allows to login to the application. Return the session.

   **Example request**:

   .. sourcecode:: http

      POST /sessions HTTP/1.1
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
        "login": 'jdp',
        "first_name": 'Jean',
        "last_name": 'Dupont',
        "avatar": "jdupont.jpg",
        "email": "jdupont@caliopen.org",
        "token": "ArfF9jApDZpOjP8WG"
      }

   :reqheader X-device: The user's current type of device
   :statuscode 200: no error
   :statuscode 403: bad credentials


.. http:delete:: /sessions/(string:token)

   Delete the session identified by `token` to logout of the application.

   **Example request**:

   .. sourcecode:: http

      DELETE /sessions/ArfF9jApDZpOjP8WG HTTP/1.1
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
        "status": "ok"
      }

   :statuscode 200: no error
   :statuscode 404: session not found


.. http:get:: /threads

   List of the threads. A thread is the container of a set of messages.

   **Example request**:

   .. sourcecode:: http

      GET /threads HTTP/1.1
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [{
        "id": 1,
        "date_updated": "2013-15-01 14:01:21",
        "text": "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
        "recipients": [{
          'first_name': 'jean',
          'last_name': 'dupont'
        }],
        "attachments": [{
          'file': 'afile.pdf',
          'content_type': 'application/pdf'
        }],
        "labels": ['work', 'projectX'],
        "security": 80
      }]

   :query token: session token.
   :query sort: one of:

    - date_updated asc
    - date_updated desc

   :query page: page number. default is 0
   :query limit: limit number. default is 30
   :query filter: a dict of filters. default is {}. Available filters :

    - ``{'labels': [1, 3, 5]}``

   :statuscode 200: no error


.. http:get:: /threads/(int:thread_id)/messages

   List the messages of the thread `thread_id`.

   **Example request**:

   .. sourcecode:: http

      GET /threads/42/messages HTTP/1.1
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [{
        "id": 2,
        "title": "Lorem ipsum dolor sit amet.",
        "body": "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
        "date_sent": "2013-15-01 14:01:21",
        "protocole": "email",
        "attachments": [{
          'file': 'afile.pdf',
          'content_type': 'application/pdf'
        }],
        "security": 80,
        "offset": 1,
        "answer_message_id": 1,
        "thread_id": 42
      }]

   :query token: session token.
   :statuscode 200: no error
   :statuscode 404: the thread has not been found


.. http:post:: /threads/(int:thread_id)/messages

   Create a new message in the thread `thread_id`.

   **Example request**:

   .. sourcecode:: http

      POST /threads/42/messages HTTP/1.1
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      [{
        "id": 10,
        "title": "Lorem ipsum dolor sit amet.",
        "body": "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
        "date_sent": "2013-15-01 14:01:21",
        "protocole": "email",
        "attachments": [{
          'file': 'afile.pdf',
          'content_type': 'application/pdf'
        }],
        "security": 80,
        "offset": 1,
        "answer_message_id": 1,
        "thread_id": 42
      }]

   :query token: session token.
   :query title: the title of the message
   :query body: the body of the message
   :query protocole: the protocole used to send the message
   :query attachments: list of files attached to the message

     ::

      [{
        'file': 'afile.pdf',
        'content_type': 'application/pdf',
        'bynary_data': XXX
      }]

   :query message_id: the ID of the message to which the message answers
   :statuscode 200: no error
   :statuscode 404: the thread has not been found
