from __future__ import absolute_import, unicode_literals

import os

from pyramid.response import Response

# XXX a better context management
from cqlengine import connection
from caliop.config import Configuration
Configuration.load(
    './sandbox/conf.yaml',
    'global')
connection.setup(['127.0.0.1:9160'])

from caliop.helpers.log import log
from caliop.helpers.json import to_json

from caliop.core.user import User
from caliop.core.thread import Thread as UserThread
from caliop.core.message import Message as UserMessage
from caliop.core.contact import Contact as UserContact


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


class Thread(Api):

    def __call__(self):
        user = User.get(self.request.session['user'])
        thread_id = int(self.request.matchdict.get('thread_id'))
        thread = UserThread.by_id(user, thread_id)
        log.debug('Got thread %r' % thread)
        return Response(to_json(thread))


class Threads(Thread):
    def __call__(self):
        # XXX : user request session
        user = User.get(self.request.session['user'])
        threads = UserThread.by_user(user)
        return Response(to_json(threads))


class ThreadMessages(Api):

    def __call__(self):
        user = User.get(self.request.session['user'])
        thread_id = int(self.request.matchdict.get('thread_id'))

        messages = UserMessage.by_thread_id(user, thread_id)
        return Response(to_json(messages))


class ContactLogin(Api):

    def __call__(self):
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            user = User.authenticate(credentials['login'],
                                     credentials['password'])
            self.request.session['user'] = user.id
            return Response(to_json(user.to_api()))

        except (KeyError, BadCredentials, Exception), exc:
            # XXX raise correct exception in authenticate
            log.error('Authentication failed for %s : %r' %
                      (credentials['login'], exc))
            return Response('BadCredentials', status='403 Forbidden')


class ContactInfo(Api):

    def __call__(self):
        user = User.get(self.request.session['user'])
        return Response(to_json(user.to_api()))


class Contacts(Api):

    def contact_link(self, contact):
        name = None
        if not (contact.last_name or contact.first_name):
            if contact.infos.get('full_name'):
                name = contact.infos['full_name']
            elif contact.infos.get('mail'):
                name = contact.infos['mail']
            elif contact.info.get('phone'):
                name = contact.infos['phone']
        return {'id': contact.id, 'name': name}

    def __call__(self):
        user = User.get(self.request.session['user'])
        groups = UserContact.list_by_group(user)
        results = []
        for g, contacts in groups.iteritems():
            results.append({
                'group': g,
                'contacts': [self.contact_link(x) for x in contacts]})
        results = sorted(results, key=lambda x: x['group'])
        return Response(to_json(results))
