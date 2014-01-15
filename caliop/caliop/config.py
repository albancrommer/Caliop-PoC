#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from pyramid_jinja2 import renderer_factory


def includeme(config):
    settings = config.registry.settings

    config.include('pyramid_jinja2')
    config.add_renderer('.html', renderer_factory)

    rootpath = os.path.dirname(os.path.realpath(__file__))

    # configure templates dir (angular build dir)
    template_path = os.path.join(rootpath, '../../caliop.ng/build')
    config.add_jinja2_search_path(template_path)

    # configure static dir on the same dir (angular build dir)
    static_path = os.path.join(rootpath, 'static')
    config.add_static_view('/static', template_path)
