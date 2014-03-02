from caliop.helpers.log import log
from caliop.mda.message import MdaMessage
from caliop.core.message import Message, MessagePart
from caliop.core.thread import Thread
from caliop.core.contact import ContactLookup

import random
RANDOM_TAGS = ['WORK', 'PERSONAL', 'INBOX', 'SPAM',
               'IMPORTANT', 'URGENT']


class DeliveryAgent(object):
    """Main logic for delivery of a mail message"""

    exclude_parts = ['multipart/mixed', 'multipart/alternative']

    def _resolve_user_contacts(self, user, mail):
        """Find all contacts known in the mail"""
        contacts = []
        for addr in mail.all_recipients():
            if addr != user.id:
                log.debug('Try to resolve contact %s' % addr)
                contact = ContactLookup.get(user, addr)
                contacts.append(contact)
        return contacts

    def _get_tags(self, user, mail):
        # XXX: real logic needed
        tags = ['MAIL']
        tags.extend(random.sample(RANDOM_TAGS, 2))
        return tags

    def process_user_mail(self, user, mail, parts):
        # XXX : logic here, for user rules etc
        contacts = self._resolve_user_contacts(user, mail)
        log.debug('Found %d contacts' % len(contacts))
        msg = mail.mail
        tags = self._get_tags(user, mail)
        security_level = random.randint(20, 100)
        thread = Thread.from_mail(user, msg, contacts, tags)
        return Message.create_from_mail(user, msg, parts,
                                        contacts, tags,
                                        thread.thread_id,
                                        security_level)

    def process(self, buf):
        """
        Process a mail from buffer, to deliver it to users that can be found
        """
        mail = MdaMessage(buf)

        messages = []
        parts = []
        if mail.parts and mail.users:
            for part in mail.parts:
                if not part.get_content_type() in self.exclude_parts:
                    part = MessagePart.create(part, mail.users)
                    log.debug('Created part %s (%s)' %
                              (part.id, part.content_type))
                    part.save()
                    parts.append(part)
        if mail.users:
            for user in mail.users:
                message = self.process_user_mail(user, mail, parts)
                if message:
                    log.debug('Delivery OK for message %s:%d' %
                              (user.id, message.message_id))
                    messages.append(message)
        return messages
