# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from .api import API




class Tag(API):
    filename = 'tags.json'

    def get(self, property_name, value):
        tags = json.loads(self.read_json())
        tags = [tag for tag in tags if tag[property_name] == value]

        if not tags:
            return HTTPNotFound()

        return Response(json.dumps(tags[0]))


class TagById(Tag):
    def get(self):
        tag_id = int(self.request.matchdict.get('tag_id'))
        return super(TagById, self).get('id', tag_id)


class TagByLabel(Tag):
    def get(self):
        tag_label = self.request.matchdict.get('tag_label')
        return super(TagByLabel, self).get('label', tag_label)


class Tags(Tag):
    def get(self):
        tags = json.loads(self.read_json())
        return Response(json.dumps(tags))
