from caliop.mda.message import Message as Mail
from caliop.core.message import Message


class DeliveryAgent(object):
    """Main logic for delivery of a mail message"""

    def __init__(self, conf):
        self.conf = conf

    def process_user(self, user, mail):
        # XXX : logic here, for user rules etc
        return Message.create(user, mail.mail)

    def process(self, buf):
        """
        Process a mail from buffer, to deliver it to users that can be found
        """
        mail = Mail(buf)

        messages = []
        if mail.users:
            for user in mail.users:
                message = self.process_user(user, mail)
                if message:
                    messages.append(message)
        return messages
