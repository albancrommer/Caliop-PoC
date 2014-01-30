from __future__ import absolute_import, unicode_literals

import os
import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPMethodNotAllowed


class API(object):
    filename = None
    request = None

    def __init__(self, request):
        self.request = request
        self.init()

    def init(self):
        pass

    def get_path(self, **kw):
        rootpath = os.path.dirname(os.path.realpath(__file__))
        filename = kw.get('filename', self.filename)
        return os.path.join(rootpath, 'json', filename)

    def read_json(self, **kw):
        filename = kw.get('filename', self.filename)
        path = self.get_path(filename=filename)

        stream = open(path)
        json = stream.read()
        stream.close()

        return json

    def __call__(self):
        try:
            return getattr(self, self.request.method.lower())()
        except AttributeError:
            return HTTPMethodNotAllowed()
