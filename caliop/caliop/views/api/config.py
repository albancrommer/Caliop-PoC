#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid_jinja2 import renderer_factory
# XXX : use a real session factory
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from caliop.helpers import renderer


def includeme(config):
    """
    Serve a static JSON based REST API.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config.set_session_factory(my_session_factory)

    config.commit()
    config.add_renderer('text_plain', renderer.TextPlainRenderer)
    config.add_renderer('json', renderer.JsonRenderer)
    config.add_renderer('simplejson', renderer.JsonRenderer)
    config.add_renderer('part', renderer.PartRenderer)

    # Activate cornice in any case and scan
    config.scan('caliop.views.api.api')

    config.add_route('contact.info', '/api/mock/contact/info')
    config.add_view('caliop.views.api.ContactInfo',
                    route_name='contact.info',
                    renderer='json')

    config.add_route('contact.login', '/api/mock/contact/login')
    config.add_view('caliop.views.api.ContactLogin',
                    route_name='contact.login',
                    renderer='json')
