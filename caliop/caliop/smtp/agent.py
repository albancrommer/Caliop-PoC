from caliop.helpers.log import log
from caliop.smtp.message import MdaMessage
from caliop.core.raw import RawMail
from caliop.core.user import UserMessage
from caliop.core.message import Message, MessagePart
from caliop.core.contact import ContactLookup, Recipient

import random


class DeliveryAgent(object):
    """Main logic for delivery of a mail message"""

    def _resolve_user_contacts(self, user, msg):
        """Find all contacts known in the mail"""
        contacts = []
        for type, recips in msg.recipients.iteritems():
            for addr, real_addr in recips:
                if addr != user.user_id:
                    log.debug('Try to resolve contact %s' % addr)
                    contact = ContactLookup.get(user, addr)
                    contacts.append(Recipient(contact, real_addr, type))
        return contacts

    def _get_tags(self, user, mail):
        # XXX: real logic needed
        tags = ['MAIL']
        user_tags = [x.label for x in user.tags if x.label != 'MAIL']
        tags.extend(random.sample(user_tags, 2))
        return tags

    def process_user_mail(self, user, msg, parts):
        # XXX : logic here, for user rules etc
        contacts = self._resolve_user_contacts(user, msg)
        log.debug('Found %d contacts' % len(contacts))
        tags = self._get_tags(user, msg)
        security_level = random.randint(20, 100)
        user_msg = UserMessage(user, msg, security_level,
                               contacts, tags, parts)
        return Message.from_user_message(user_msg)

    def process(self, buf):
        """
        Process a mail from buffer, to deliver it to users that can be found
        """
        msg = MdaMessage(buf)

        messages = []
        parts = []
        if msg.users:
            user_ids = set(x.user_id for x in msg.users)
            raw = RawMail.create(msg.message_id,
                                 user_ids,
                                 msg.mail.as_string())
            log.debug('Created raw mail %r' % raw.raw_id)
        if msg.parts and msg.users:
            cpt = 0
            for part in msg.parts:
                if not part.is_multipart():
                    new_part = MessagePart.create(part, msg.users, cpt)
                    log.debug('Created part %s (%s)' %
                              (new_part.id, new_part.content_type))
                    new_part.save()
                    parts.append(new_part)
                    cpt += 1
        if msg.users:
            for user in msg.users:
                message = self.process_user_mail(user, msg, parts)
                if message:
                    log.debug('Delivery OK for message %s:%d' %
                              (user.user_id, message.message_id))
                    messages.append(message)
        return messages
