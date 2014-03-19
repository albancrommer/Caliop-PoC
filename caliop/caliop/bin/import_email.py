#!/usr/bin/env python

"""
This script parse for a user (first arg) a mbox file (second arg)
and import mails

- create user if needed
- resolve all contacts

"""
import os
from email import message_from_file
from os import listdir
from mailbox import mbox, Maildir


def import_email(email, import_path, format):

    from caliop.helpers.log import log
    from caliop.core.user import User
    from caliop.core.contact import Contact, ContactLookup
    from caliop.smtp.agent import DeliveryAgent
    from caliop.smtp.message import MdaMessage

    AVATAR_DIR = '../../caliop.ng/src/assets/images/avatars'

    if format == 'maildir':
        emails = Maildir(import_path, factory=message_from_file)
        mode = 'maildir'
    else:
        if os.path.isdir(import_path):
            mode = 'mbox_directory'
            emails = {}
            files = [f for f in listdir(import_path) if \
                os.path.isfile(os.path.join(import_path, f))]
            for f in files:
                with open('%s/%s' % (import_path, f)) as fh:
                    emails[f] = message_from_file(fh)
        else:
            mode = 'mbox'
            emails = mbox(import_path)

    try:
        user = User.get(email)
    except Exception:
        log.info("Creating user")
        user = User.create(user_id=email,
                           first_name='Test %s' % email.upper(),
                           last_name=email.lower(),
                           password='123456')
        user.save()

    agent = DeliveryAgent()
    mailfrom = ''
    rcpts = [email]

    log.info("Processing mode %s" % mode)
    msgs = []
    for key, mail in emails.iteritems():
        # Create contact for user
        log.info('Processing mail %s' % key)
        msgs.append(MdaMessage(rcpts, mail))

    msgs = sorted(msgs, key=lambda msg: msg.date)

    for msg in msgs:
        for type, addresses in msg.recipients.iteritems():
            if not addresses:
                continue
            for alias, _address in addresses:
                lookup = ContactLookup.get(user, alias)
                if not lookup:
                    log.info('Creating contact %s' % alias)
                    infos = {'mail': alias}
                    name, domain = alias.split('@')

                    if os.path.isfile('%s/%s.png' % (AVATAR_DIR, name)):
                        infos.update({'avatar': '%s.png' % name})
                    Contact.create(user, infos)
        res = agent.process(mailfrom, rcpts, msg.mail)
        log.info('Process result %r' % res)
