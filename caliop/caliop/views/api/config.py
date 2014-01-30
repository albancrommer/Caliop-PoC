#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid_jinja2 import renderer_factory


def includeme(config):
    """
    Serve a static JSON based REST API.
    """

    config.add_route('sessions', '/api/mock/sessions')
    config.add_view('caliop.views.api.Sessions',
        request_method=('POST', 'DELETE'),
        route_name='sessions',
        renderer='json')

    config.add_route('threads', '/api/mock/threads')
    config.add_view('caliop.views.api.Threads',
        request_method=('GET',),
        route_name='threads',
        renderer='json')

    config.add_route('messages', '/api/mock/threads/{thread_id}/messages')
    config.add_view('caliop.views.api.Messages',
        request_method=('GET', 'POST',),
        route_name='messages',
        renderer='json')

    config.add_route('contact.info', '/api/mock/contact/info')
    config.add_view('caliop.views.api.ContactInfo', route_name='contact.info', renderer='json')


