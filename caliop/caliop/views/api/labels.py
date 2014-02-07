# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response

from .api import API




class Label(API):
    filename = 'labels.json'

    def get(self):
        label_id = int(self.request.matchdict.get('label_id'))

        labels = json.loads(self.read_json())
        labels = [label for label in labels if label['id'] == label_id]

        if not labels:
            return HTTPNotFound()

        return Response(json.dumps(labels[0]))


class Labels(Label):
    def get(self):
        labels = json.loads(self.read_json())
        return Response(json.dumps(labels))
