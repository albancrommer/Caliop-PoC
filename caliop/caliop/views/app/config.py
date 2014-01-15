#-*- coding: utf-8 -*-

from __future__ import unicode_literals


def includeme(config):
    """
    Serve the Angular app.
    """
    config.add_route('app.index', '/')
    config.add_view('caliop.views.app.index',
                    route_name='app.index',
                    renderer='index.html',
                    )
