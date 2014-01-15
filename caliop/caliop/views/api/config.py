#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from pyramid_jinja2 import renderer_factory


def includeme(config):
    """
    Serve a static JSON based REST API.
    """

    config.add_route('messages', '/api/mock/messages')
    config.add_view('caliop.views.api.Messages', route_name='messages', renderer='json')

    # config.add_route('vm_info', '/mock/hosting/info/471')
    # config.add_view('mustela.web.views.mock.VmInfo', route_name='vm_info', renderer='json')

