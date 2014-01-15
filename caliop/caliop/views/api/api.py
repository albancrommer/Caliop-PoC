import os

from pyramid import threadlocal
from pyramid.response import Response


class Api(object):
    def __init__(self, request):
        self.request = request

    def __call__(self):
        rootpath = os.path.dirname(os.path.realpath(__file__))
        jsonfile = os.path.join(rootpath, 'json', self.filename)

        return Response(open(jsonfile).read())


class Messages(Api):
    filename = 'messages.json'
