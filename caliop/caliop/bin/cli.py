#!/usr/bin/env python

"""
This script parse for a user (first arg) a mbox file (second arg)
and import mails

- create user if needed
- resolve all contacts

"""
import sys
import argparse
from cqlengine import connection

from pyramid.paster import get_appsettings, setup_logging
from pyramid.config import Configurator

from caliop import includeme as include_caliop
from caliop.core.config import includeme as include_caliop_core

from caliop.bin.import_email import import_email
from caliop.bin.setup_storage import setup_storage

def main(args=sys.argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='conffile', default='caliop.yaml')
    subparsers = parser.add_subparsers(title="action")

    sp_import = subparsers.add_parser('import', help='import existing mailbox')
    sp_import.set_defaults(func=import_email)
    sp_import.add_argument('-f', dest='format',  choices=['mbox', 'maildir'],
                           default='mbox')
    sp_import.add_argument('-p', dest='import_path')
    sp_import.add_argument('-e', dest='email')

    sp_setup_storage = subparsers.add_parser('setup',
        help='initialize the storage engine')
    sp_setup_storage.set_defaults(func=setup_storage)

    kwargs = parser.parse_args(args[1:])
    kwargs = vars(kwargs)

    config_uri = kwargs.pop('conffile')
    setup_logging(config_uri)

    settings = get_appsettings(config_uri, u'main')
    # do not declare routes and others useless includes
    del settings['pyramid.includes']

    config = Configurator(settings=settings)
    include_caliop(config)
    include_caliop_core(config)
    config.end()

    func = kwargs.pop('func')
    func(**kwargs)


if __name__ == '__main__':
    main()
