import smtplib
import uuid
from email.mime.text import MIMEText
from itertools import groupby

from caliop.core.message import Message


class MailSender(object):
    """Make a new mail from a message instance"""

    def new_message_id(self, user_id):
        return '<%s-%s>' % (str(uuid.uuid4()), user_id)

    def process_recipients(self, contacts, mail):

        def sort_key(contact):
            return contact['type']

        data = sorted(contacts, key=sort_key)
        for t, g in groupby(data, key=sort_key):
            group = list(g)
            # XXX : resolve contact for real name, or must get from address
            # full value from original mail
            mail[t.title()] = ', '.join(group)

    def process(self, user_id, message_id):
        message = Message.index_by_id(user_id, message_id)
        if not message:
            raise Exception('No message found in index %s:%s' %
                            (user_id, message_id))
        msg = MIMEText(message.text, _charset='utf-8')
        msg['Subject'] = message.subject
        msg['From'] = user_id
        msg['Date'] = message.date
        msg['Message-Id'] = self.new_message_id(user_id)
        # TOFIX: got such value from index ?
        #if message.parent_message_id:
        #    msg['In-Reply-To'] = message.parent_message_id
        self.process_recipients(message.contacts, msg)
        return msg.as_string()
        # XXX : for later
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(user_id, msg['To'], msg.as_string())
