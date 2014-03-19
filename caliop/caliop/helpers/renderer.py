import simplejson as json
import datetime
from decimal import Decimal

from zope.interface import implementer
from pyramid.interfaces import ITemplateRenderer


@implementer(ITemplateRenderer)
class TextPlainRenderer(object):

    def __init__(self, request):
        self.request = request

    def __call__(self, value, system):
        request = system['request']
        request.response.content_type = b'text/plain'
        return value


class JSONEncoder(json.JSONEncoder):
    _datetypes = (datetime.date, datetime.datetime)

    def default(self, obj):
        '''Convert object to JSON encodable type.'''
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, self._datetypes):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)


@implementer(ITemplateRenderer)
class JsonRenderer(object):
    """
    Template Factory for render json that accept datetime and decimal.
    """

    def __init__(self, _renderer_helper):
        pass

    def __call__(self, data, context):
        acceptable = ('application/json', 'text/json', 'text/plain')
        response = context['request'].response
        content_type = (context['request'].accept.best_match(acceptable)
                        or acceptable[0])
        response.content_type = content_type
        return json.dumps(data, cls=JSONEncoder)
