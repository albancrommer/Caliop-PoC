from __future__ import absolute_import, unicode_literals

from pyramid.response import Response
from cornice.resource import resource

from caliop.config import Configuration
from caliop.helpers.log import log
from caliop.helpers.json import to_json

from caliop.core.user import User
from caliop.core.thread import Thread as UserThread
from caliop.core.message import Message as UserMessage
from caliop.core.contact import Contact as UserContact


DEFAULT_LIMIT = Configuration('global').get('site.item_per_page')
BASE_URL = Configuration('global').get('api.url', '/api/mock')


def make_url(url):
    # XXX : should use cornice.route_prefix configuration
    return '%s%s' % (BASE_URL, url)


def get_limit(request):
    limit = {}
    limit['size'] = request.matchdict.get('limit', DEFAULT_LIMIT)
    limit['from'] = request.matchdict.get('from_index', 0)
    return limit


def check_user(request):
    # XXX : use a validator and do a real check
    return User.get(request.session['user'])


@resource(collection_path=make_url('/threads'),
          path=make_url('/threads/{thread_id}'))
class Thread(object):

    def __init__(self, request):
        self.request = request
        self.user = check_user(request)

    def collection_get(self):
        threads = UserThread.by_user(self.user, limit=get_limit(self.request))
        return Response(to_json(threads))

    def get(self):
        thread_id = int(self.request.matchdict.get('thread_id'))
        thread = UserThread.by_id(self.user, thread_id)
        return Response(to_json(thread))


@resource(collection_path=make_url('/threads/{thread_id}/messages'),
          path=make_url('/threads/{thread_id}/messages/{message_id}'))
class Message(object):

    def __init__(self, request):
        self.request = request
        self.user = check_user(request)

    def collection_get(self):
        thread_id = int(self.request.matchdict.get('thread_id'))
        messages = UserMessage.by_thread_id(self.user, thread_id,
                                            limit=get_limit(self.request))
        return Response(to_json(messages))


@resource(collection_path=make_url('/contacts'),
          path=make_url('/contacts/{contact_id'))
class Contact(object):

    def __init__(self, request):
        self.request = request
        self.user = check_user(request)

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

    def collection_get(self):
        groups = UserContact.list_by_group(self.user)
        results = []
        for g, contacts in groups.iteritems():
            results.append({
                'group': g,
                'contacts': [self.contact_link(x) for x in contacts]})
        results = sorted(results, key=lambda x: x['group'])
        return Response(to_json(results))


# XXX XXX XXX XXX Should not be here !!!!
class Api(object):

    def __init__(self, request):
        self.request = request


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
