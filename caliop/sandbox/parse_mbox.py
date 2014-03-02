#!/usr/bin/env python

"""
This script parse for a user (first arg) a mbox file (second arg)
and import mails

- create user if needed
- resolve all contacts

"""
import sys
from mailbox import mbox

from cqlengine import connection
from caliop.config import Configuration
Configuration.load('./conf.yaml', 'global')

from caliop.core.user import User
from caliop.core.contact import Contact, ContactLookup
from caliop.mda.agent import DeliveryAgent
from caliop.mda.message import MdaMessage

connection.setup(['127.0.0.1:9160'])

user = sys.argv[1]
filename = sys.argv[2]
m = mbox(filename)

try:
    user = User.get(user)
except:
    print "Creating user"
    user = User.create(id=user,
                       first_name='Test %s' % user.upper(),
                       last_name=user.lower(),
                       password='123456')
    user.save()

agent = DeliveryAgent()

for mail in m.values():
    # Create contact for user
    msg = MdaMessage(mail)
    for rec in msg.all_recipients():
        lookup = ContactLookup.get(user, rec)
        if not lookup:
            print "Creating contact %s" % rec
            Contact.create(user, {'mail': rec})
    res = agent.process(mail)
    print "Process result %r" % res
