from caliop.helpers.log import log
from caliop.mda.message import Message as Mail
from caliop.core.message import Message, MessagePart


class DeliveryAgent(object):
    """Main logic for delivery of a mail message"""

    exclude_parts = ['multipart/mixed', 'multipart/alternative']

    def __init__(self, conf):
        self.conf = conf

    def process_user_mail(self, user, mail, parts):
        # XXX : logic here, for user rules etc
        return Message.create_from_mail(user, mail, parts)

    def process(self, buf):
        """
        Process a mail from buffer, to deliver it to users that can be found
        """
        mail = Mail(buf)

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
                message = self.process_user_mail(user, mail.mail, parts)
                if message:
                    log.debug('Delivery OK for message %s:%d' %
                              (user.id, message.message_id))
                    messages.append(message)
        return messages
