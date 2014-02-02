import logging

from caliop.config import Configuration

try:
    from logging.config import dictConfig
    dictConfig(Configuration('global').get('logging'))
    log = logging.getLogger('caliop')
except:
    log = logging.getLogger(__name__)
