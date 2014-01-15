import logging

from .config import includeme  # used by pyramid

from pyramid.httpexceptions import HTTPFound


log = logging.getLogger(__name__)


def index(request):
    """
    Angular root index.
    """

    return {}
