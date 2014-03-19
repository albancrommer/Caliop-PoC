from __future__ import absolute_import, unicode_literals

from datetime import datetime

from pyramid.response import Response
from cornice.resource import resource

from caliop.config import Configuration
from caliop.helpers.log import log
from caliop.helpers.json import to_json

from caliop.core.raw import RawMail
from caliop.core.user import User, UserMessage
from caliop.core.thread import Thread as UserThread
from caliop.core.message import (Message as CMessage, BaseMessage)
from caliop.core.contact import Contact as UserContact, Recipient


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


class Api(object):
    """Base class for all Api"""

    def __init__(self, request):
        self.request = request

    def check_user(self):
        return User.get(self.request.session['user'])


@resource(collection_path=make_url('/threads'),
          path=make_url('/threads/{thread_id}'))
class Thread(Api):

    def __init__(self, request):
        self.request = request
        self.user = self.check_user()

    def collection_get(self):
        threads = UserThread.by_user(self.user, limit=get_limit(self.request))
        return Response(to_json(threads))

    def get(self):
        thread_id = int(self.request.matchdict.get('thread_id'))
        thread = UserThread.by_id(self.user, thread_id)
        return Response(to_json(thread))


@resource(collection_path=make_url('/threads/{thread_id}/messages'),
          path=make_url('/threads/{thread_id}/messages/{message_id}'))
class Message(Api):

    def __init__(self, request):
        self.request = request
        self.user = self.check_user()

    def extract_recipients(self):
        """Get recipients from request"""
        recipients = {}
        for rec_type in ['to_recipients', 'cc_recipients', 'bcc_recipients']:
            addrs = []
            for rec in self.request.json.get(rec_type, []):
                addrs.append((rec['contact'], rec['address']))
            recipients[rec_type] = addrs
        recipients['from'] = [(self.user.user_id, self.user.user_id)]
        return recipients

    def collection_get(self):
        thread_id = int(self.request.matchdict.get('thread_id'))
        messages = CMessage.by_thread_id(self.user, thread_id,
                                         limit=get_limit(self.request))
        return Response(to_json(messages))

    def collection_post(self):
        thread_id = int(self.request.matchdict.get('thread_id'))
        reply_to = self.request.json.get('reply_to')
        if reply_to:
            parent = CMessage.get(self.user, reply_to)
            parent_message_id = parent.external_id
            thread_id = parent.thread_id
            sec_level = parent.security_level
        else:
            parent_message_id = None
            thread_id = None
            # XXX : how to compute ?
            sec_level = 0
        recipients = self.extract_recipients()
        # XXX : make recipient for UserMessage using Recipient class
        print "Recipients %r" % recipients
        subject = self.request.json.get('subject')
        text = self.request.json.get('text')
        tags = self.request.json.get('tags', [])
        base_msg = BaseMessage(recipients,
                               subject=subject,
                               text=text, tags=tags,
                               date=datetime.utcnow(),
                               security_level=sec_level,
                               thread_id=thread_id,
                               parent_message_id=parent_message_id)
        user_msg = UserMessage(self.user, base_msg, sec_level,
                               [], tags, [])
        msg = CMessage.from_user_message(user_msg)
        idx_msg = CMessage.by_id(self.user, msg.message_id)
        log.info('Post new message %r' % msg.message_id)
        # XXX return redirect to newly created message ?
        return Response(to_json(idx_msg))


@resource(collection_path=make_url('/contacts'),
          path=make_url('/contacts/{contact_id'))
class Contact(Api):

    def __init__(self, request):
        self.request = request
        self.user = self.check_user()

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


@resource(path=make_url('/mails/{raw_id}'))
class Raw(Api):

    def __init__(self, request):
        self.request = request
        self.user = self.check_user()

    def get(self):
        raw_id = self.request.matchdict.get('raw_id')
        raw = RawMail.get(raw_id)
        if not self.user.user_id in raw.users:
            return Response(to_json({'error': 'Not allowed'}))
        return Response(raw.data)


# XXX XXX XXX XXX Should not be here !!!!
class ContactLogin(Api):

    def __call__(self):
        credentials = self.request.json

        class BadCredentials(Exception):
            pass

        try:
            user = User.authenticate(credentials['login'],
                                     credentials['password'])
            self.request.session['user'] = user.user_id
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
