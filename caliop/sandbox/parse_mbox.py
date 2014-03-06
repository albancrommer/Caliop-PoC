#!/usr/bin/env python

"""
This script parse for a user (first arg) a mbox file (second arg)
and import mails

- create user if needed
- resolve all contacts

"""
import sys
import os
from os import listdir
from mailbox import mbox
from email.parser import Parser
from cqlengine import connection
from caliop.config import Configuration
Configuration.load('./conf.yaml', 'global')

from caliop.helpers.log import log
from caliop.core.user import User
from caliop.core.contact import Contact, ContactLookup
from caliop.mda.agent import DeliveryAgent
from caliop.mda.message import MdaMessage

from logging.config import dictConfig
dictConfig(Configuration('global').get('logging'))

connection.setup(['127.0.0.1:9160'])

user = sys.argv[1]
filename = sys.argv[2]

if os.path.isdir(filename):
    mode = 'directory'
    m = {}
    files = [f for f in listdir(filename) if \
        os.path.isfile(os.path.join(filename, f))]
    parser = Parser()
    for f in files:
        m[f] = parser.parse(open('%s/%s' % (filename, f)))
else:
    mode = 'mbox'
    m = mbox(filename)

try:
    user = User.get(user)
except:
    log.info("Creating user")
    user = User.create(id=user,
                       first_name='Test %s' % user.upper(),
                       last_name=user.lower(),
                       password='123456')
    user.save()

agent = DeliveryAgent()

log.info("Processing mode %s" % mode)
for key, mail in m.iteritems():
    # Create contact for user
    log.info('Processing mail %s' % key)
    msg = MdaMessage(mail)
    for rec in msg.all_recipients():
        lookup = ContactLookup.get(user, rec)
        if not lookup:
            log.info("Creating contact %s" % rec)
            Contact.create(user, {'mail': rec})
    res = agent.process(mail)
    log.info("Process result %r" % res)
