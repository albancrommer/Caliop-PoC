#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

import os

from pyramid.settings import aslist
from pyramid_jinja2 import renderer_factory

from caliop.helpers.config import Configuration


def includeme(config):
    settings = config.registry.settings

    config.include('pyramid_jinja2')
    config.add_renderer('.html', renderer_factory)

    # XXX should be removed
    rootpath = os.path.dirname(os.path.realpath(__file__))

    # configure templates dir (angular build dir)
    template_path = os.path.join(rootpath, settings['caliop.ng.path'])
    config.add_jinja2_search_path(template_path)

    # configure static dir on the same dir (angular build dir)
    static_path = os.path.join(rootpath, 'static')
    config.add_static_view('/static', template_path)

    for file in aslist(settings['caliop.config']):
        name, path = file.split(':', 1)
        Configuration.load(path, name)
