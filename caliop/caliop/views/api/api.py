from __future__ import absolute_import, unicode_literals

import os
import json

from pyramid.response import Response
from pyramid.httpexceptions import HTTPMethodNotAllowed, HTTPNotFound


class API(object):
    filename = None
    request = None

    def __init__(self, request):
        self.request = request
        self.init()

    def init(self):
        """
        Optional init.
        """
        pass

    def get_path(self, **kw):
        """
        Return the path of the json file.
        """
        rootpath = os.path.dirname(os.path.realpath(__file__))
        filename = kw.get('filename', self.filename)
        return os.path.join(rootpath, 'json', filename)

    def read_json(self, **kw):
        """
        Read the json file and return its content.
        """
        filename = kw.get('filename', self.filename)
        path = self.get_path(filename=filename)

        stream = open(path)
        json = stream.read()
        stream.close()

        return json

    def add_to_json(self, entry):
        """
        Push an entry at the end of the json file.
        Return a fake ID by counting the number of items in the JSON struct.
        """
        entries = json.loads(self.read_json())
        entry['id'] = len(entries) + 1
        entries.append(entry)

        with open(self.get_path(), 'w') as jsonfile:
            jsonfile.truncate()
            json.dump(entries, jsonfile, indent=True)

        return entry['id']

    def update_to_json(self, id, entry):
        """
        Update an entry of the json file.
        """
        entries = json.loads(self.read_json())
        foundEntries = [e for e in entries if int(e['id']) == id]

        if not foundEntries:
            return False

        # remove the old dict
        entry_ = foundEntries[0]
        entries.remove(entry_)

        # add the new one
        entry_.update(entry)
        entries.append(entry_)

        with open(self.get_path(), 'w') as jsonfile:
            jsonfile.truncate()
            json.dump(entries, jsonfile, indent=True)

        return entry_

    def __call__(self):
        """
        Call the view to trigger the method which implements the requested
        HTTP verb.
        """
        try:
            return getattr(self, self.request.method.lower())()
        except AttributeError:
            return HTTPMethodNotAllowed()
