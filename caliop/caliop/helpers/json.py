import simplejson as json
import datetime
from decimal import Decimal


class JSONEncoder(json.JSONEncoder):
    _datetypes = (datetime.date, datetime.datetime)

    def default(self, obj):
        '''Convert object to JSON encodable type.'''
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, self._datetypes):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)


def to_json(data):
    """json dump using a specific encoder"""
    return json.dumps(data, cls=JSONEncoder)
