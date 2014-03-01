from caliop.helpers.log import log
from caliop.mda.message import MdaMessage
from caliop.core.message import Message, MessagePart
from caliop.core.thread import Thread
from caliop.core.contact import ContactLookup


class DeliveryAgent(object):
    """Main logic for delivery of a mail message"""

    exclude_parts = ['multipart/mixed', 'multipart/alternative']

    def _resolve_user_contacts(self, user, mail):
        """Find all contacts known in the mail"""
        contacts = []
        for addr in mail.all_recipients():
            log.debug('Try to resolve contact %s' % addr)
            try:
                contact = ContactLookup.get(user, addr)
                contacts.append(contact)
            except:
                # XXX filter only not found
                pass
        return contacts

    def process_user_mail(self, user, mail, parts):
        # XXX : logic here, for user rules etc
        contacts = self._resolve_user_contacts(user, mail)
        log.debug('Found %d contacts' % len(contacts))
        msg = mail.mail
        thread = Thread.from_mail(user, msg, contacts)
        return Message.create_from_mail(user, msg, parts, contacts,
                                        thread.thread_id)

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
