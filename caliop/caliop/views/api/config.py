#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid_jinja2 import renderer_factory
# XXX : use a real session factory
from pyramid.session import UnencryptedCookieSessionFactoryConfig


def includeme(config):
    """
    Serve a static JSON based REST API.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config.set_session_factory(my_session_factory)
    config.add_route('threads', '/api/mock/threads')
    config.add_view('caliop.views.api.Threads', route_name='threads', renderer='json')

    config.add_route('thread', '/api/mock/threads/{thread_id}')
    config.add_view('caliop.views.api.Thread', route_name='thread', renderer='json')

    config.add_route('messages', '/api/mock/threads/{thread_id}/messages')
    config.add_view('caliop.views.api.ThreadMessages', route_name='messages', renderer='json')

    config.add_route('contact.info', '/api/mock/contact/info')
    config.add_view('caliop.views.api.ContactInfo', route_name='contact.info', renderer='json')

    config.add_route('contact.login', '/api/mock/contact/login')
    config.add_view('caliop.views.api.ContactLogin', route_name='contact.login', renderer='json')

    config.add_route('contacts.list', '/api/mock/contacts')
    config.add_view('caliop.views.api.Contacts', route_name='contacts.list', renderer='json')
