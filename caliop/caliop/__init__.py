from pyramid.config import Configurator

from .config import includeme  # used by pyramid

__version__ = '0.0.1'


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.end()
    return config.make_wsgi_app()
