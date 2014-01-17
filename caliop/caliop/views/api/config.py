#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid_jinja2 import renderer_factory


def includeme(config):
    """
    Serve a static JSON based REST API.
    """

    config.add_route('messages', '/api/mock/messages')
    config.add_view('caliop.views.api.Messages', route_name='messages', renderer='json')

    config.add_route('contact.info', '/api/mock/contact/info')
    config.add_view('caliop.views.api.ContactInfo', route_name='contact.info', renderer='json')

    config.add_route('contact.login', '/api/mock/contact/login')
    config.add_view('caliop.views.api.ContactInfo', route_name='contact.login', renderer='json')
    