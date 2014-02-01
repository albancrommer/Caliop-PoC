from datetime import datetime
from email.message import Message as mailMessage

from caliop.store import (Message as ModelMessage,
                          IndexedMessage,
                          MailIndexMessage)

from caliop.core.base import AbstractCore
from caliop.core.user import User, Counter


class Message(AbstractCore):

    _model_class = ModelMessage
    _index_class = IndexedMessage

    @classmethod
    def create_from_mail(cls, mail):
        """
        Deliver a parsed mail message to all mailboxes
        return a list of messages
        """
        if not isinstance(mail, mailMessage):
            raise Exception('Invalid mail object')
        users = [mail.get('To', [])]
        users.extend(mail.get('Cc', []))
        users.extend(mail.get('Bcc', []))
        find_users = []
        for u in users:
            try:
                # XXX : remove extension in mail to find correctly user (+)
                user = User.get(u)
                if not user in find_users:
                    find_users.append(user)
            except:
                pass
        if find_users:
            messages = []
            # XXX : Must resolve known contacts in mail
            index = MailIndexMessage(mail)

            for user in find_users:
                counter = Counter.get(user.id)
                counter.message_id += 1
                counter.save()
                msg = Message.create(user_id=user.id,
                                     message_id=counter.message_id,
                                     date_insert=datetime.utcnow(),
                                     external_id=index.message_id,
                                     thread_id=index.thread_id)
                # XXX write raw message in store using msg pkey
                messages.append(cls(msg))
                # XXX index message asynchronously ?
                cls._index_class.create_index(user.id,
                                              counter.message_id,
                                              index)
            return messages
        return []
