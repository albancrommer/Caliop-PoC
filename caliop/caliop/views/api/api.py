from __future__ import absolute_import, unicode_literals

import os
import json

from pyramid.response import Response

# XXX a better context management
from cqlengine import connection
from caliop.config import Configuration
Configuration.load(
    '/home/mric/dev/Caliop-PoC/caliop/sandbox/conf.yaml',
    'global')
connection.setup(['127.0.0.1:9160'])

from caliop.helpers.log import log

from caliop.core.user import User
from caliop.core.thread import Thread as UserThread
from caliop.core.message import Message as UserMessage


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
        json_ = stream.read()
        stream.close()

        return json_

    def __call__(self):
        return Response(self.read_json())


class Thread(Api):

    def __call__(self):
        user = User.get(self.request.session['user'])
        thread_id = int(self.request.matchdict.get('thread_id'))
        thread = UserThread.by_id(user, thread_id)
        log.debug('Got thread %r' % thread)
        return Response(json.dumps(thread))


class Threads(Thread):
    def __call__(self):
        # XXX : user request session
        user = User.get(self.request.session['user'])
        threads = UserThread.by_user(user)
        return Response(json.dumps(threads))


class ThreadMessages(Api):
    filename = 'messages.json'

    def __call__(self):
        user = User.get(self.request.session['user'])
        thread_id = int(self.request.matchdict.get('thread_id'))
        messages = UserMessage.by_thread_id(user, thread_id)
        return Response(json.dumps(messages))


class Messages(Api):
    filename = 'messages.json'


class ContactLogin(Api):
    filename = 'contact.json'

    def __call__(self):
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            user = User.authenticate(credentials['login'],
                                     credentials['password'])
            self.request.session['user'] = user.id
            return Response(json.dumps(user.to_api()))

        except (KeyError, BadCredentials, Exception), exc:
            # XXX raise correct exception in authenticate
            log.error('Authentication failed for %s : %r' %
                      (credentials['login'], exc))
            return Response('BadCredentials', status='403 Forbidden')


class ContactInfo(Api):
    filename = 'contact.json'
